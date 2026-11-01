"""Full regression tests for the Wyoming options bridge."""

from __future__ import annotations

import importlib.util
import io
import json
import os
import runpy
import sys
import tempfile
import unittest
from collections.abc import Callable
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from types import ModuleType
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "wyoming-vietnamese" / "scripts" / "apply_options.py"


def load_module() -> ModuleType:
    """Load apply_options.py without importing the hyphenated add-on directory."""
    spec = importlib.util.spec_from_file_location("apply_options", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {SCRIPT}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ao = load_module()


def assert_raises(
    exception_type: type[BaseException],
    callback: Callable[[], object],
) -> BaseException:
    """Return the exception raised by callback, failing when none is raised."""
    try:
        callback()
    except exception_type as error:
        return error
    raise AssertionError(f"Expected {exception_type.__name__}")


class LoadOptionsTests(unittest.TestCase):
    """Test load_options."""

    def test_missing_file_returns_empty_options(self) -> None:
        """A missing options file falls back to an empty mapping."""
        with tempfile.TemporaryDirectory() as temp_dir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                result = ao.load_options(Path(temp_dir) / "missing.json")

        assert result == {}
        assert "[WARN] Options file not found" in stdout.getvalue()

    def test_empty_file_returns_empty_options(self) -> None:
        """An empty options file falls back to an empty mapping."""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "options.json"
            path.write_text("", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                result = ao.load_options(path)

        assert result == {}
        assert "[WARN] Options file is empty" in stdout.getvalue()

    def test_valid_object_is_loaded(self) -> None:
        """A JSON object is returned as a dictionary."""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "options.json"
            path.write_text('{"stt_engine": "zipformer"}', encoding="utf-8")

            result = ao.load_options(path)

        assert result == {"stt_engine": "zipformer"}

    def test_non_object_is_rejected(self) -> None:
        """A JSON value other than an object is rejected."""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "options.json"
            path.write_text("[]", encoding="utf-8")

            error = assert_raises(TypeError, lambda: ao.load_options(path))

        assert "must contain a JSON object" in str(error)

    def test_invalid_json_is_rejected(self) -> None:
        """Malformed JSON propagates a JSONDecodeError."""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "options.json"
            path.write_text("{", encoding="utf-8")

            assert_raises(json.JSONDecodeError, lambda: ao.load_options(path))

    def test_os_error_is_propagated(self) -> None:
        """An unreadable path propagates an OSError."""
        with tempfile.TemporaryDirectory() as temp_dir:
            assert_raises(OSError, lambda: ao.load_options(Path(temp_dir)))


class FormatValueTests(unittest.TestCase):
    """Test format_value."""

    def test_none_is_unset(self) -> None:
        """None carries no setting."""
        assert ao.format_value(None) is None

    def test_booleans_use_lowercase(self) -> None:
        """Booleans become lowercase strings."""
        assert ao.format_value(True) == "true"
        assert ao.format_value(False) == "false"

    def test_numbers_are_converted(self) -> None:
        """Integer and float values become strings."""
        assert ao.format_value(0) == "0"
        assert ao.format_value(-1) == "-1"
        assert ao.format_value(1.5) == "1.5"

    def test_strings_are_stripped(self) -> None:
        """Surrounding whitespace is removed."""
        assert ao.format_value(" value ") == "value"

    def test_empty_strings_are_unset(self) -> None:
        """Empty and whitespace-only strings carry no setting."""
        assert ao.format_value("") is None
        assert ao.format_value("   ") is None

    def test_unsupported_types_are_rejected(self) -> None:
        """Lists and mappings are rejected."""
        assert_raises(ValueError, lambda: ao.format_value(["value"]))
        assert_raises(ValueError, lambda: ao.format_value({"value": 1}))


class BuildEnvironmentTests(unittest.TestCase):
    """Test build_environment."""

    def test_all_options_are_mapped(self) -> None:
        """Every known option maps to its server environment variable."""
        options = {
            "stt_engine": "zipformer",
            "tts_engine": "nghitts",
            "tts_voice": "ngoc-huyen-moi",
            "log_level": "debug",
        }
        stdout = io.StringIO()
        with (
            mock.patch.dict(os.environ, {"EXISTING": "1"}, clear=True),
            redirect_stdout(stdout),
        ):
            env = ao.build_environment(options)

        assert env["STT_ENGINE"] == "zipformer"
        assert env["TTS_ENGINE"] == "nghitts"
        assert env["TTS_VOICE"] == "ngoc-huyen-moi"
        assert env["LOG_LEVEL"] == "debug"
        assert env["EXISTING"] == "1"
        assert "[INFO] STT_ENGINE=zipformer" in stdout.getvalue()

    def test_missing_options_are_skipped(self) -> None:
        """Options absent from the file do not create environment variables."""
        with (
            mock.patch.dict(os.environ, {}, clear=True),
            redirect_stdout(io.StringIO()),
        ):
            env = ao.build_environment({"stt_engine": "zipformer"})

        assert env["STT_ENGINE"] == "zipformer"
        assert "TTS_ENGINE" not in env
        assert "TTS_VOICE" not in env
        assert "LOG_LEVEL" not in env

    def test_unset_values_are_skipped(self) -> None:
        """None and blank option values do not override the environment."""
        with (
            mock.patch.dict(os.environ, {"STT_ENGINE": "existing"}, clear=True),
            redirect_stdout(io.StringIO()),
        ):
            env = ao.build_environment(
                {
                    "stt_engine": None,
                    "tts_engine": "",
                    "tts_voice": "   ",
                }
            )

        assert env["STT_ENGINE"] == "existing"
        assert "TTS_ENGINE" not in env
        assert "TTS_VOICE" not in env

    def test_values_override_existing_environment(self) -> None:
        """Configured options replace inherited environment values."""
        with (
            mock.patch.dict(os.environ, {"LOG_LEVEL": "old"}, clear=True),
            redirect_stdout(io.StringIO()),
        ):
            env = ao.build_environment({"log_level": "warning"})

        assert env["LOG_LEVEL"] == "warning"

    def test_unknown_options_are_ignored(self) -> None:
        """Options not in the mapping are ignored."""
        with (
            mock.patch.dict(os.environ, {}, clear=True),
            redirect_stdout(io.StringIO()),
        ):
            env = ao.build_environment({"unknown": "value"})

        assert "unknown" not in env
        assert "UNKNOWN" not in env

    def test_boolean_and_numeric_values_are_formatted(self) -> None:
        """Non-string option values are formatted before use."""
        with (
            mock.patch.dict(os.environ, {}, clear=True),
            redirect_stdout(io.StringIO()),
        ):
            env = ao.build_environment({"stt_engine": True, "log_level": 3})

        assert env["STT_ENGINE"] == "true"
        assert env["LOG_LEVEL"] == "3"

    def test_unsupported_option_value_raises(self) -> None:
        """An unsupported option type is not silently accepted."""
        with mock.patch.dict(os.environ, {}, clear=True):
            assert_raises(
                ValueError,
                lambda: ao.build_environment({"stt_engine": ["zipformer"]}),
            )


class DropPrivilegesTests(unittest.TestCase):
    """Test drop_privileges."""

    def test_non_root_process_is_left_alone(self) -> None:
        """No privilege calls are made when already unprivileged."""
        setgroups = mock.Mock()
        setgid = mock.Mock()
        setuid = mock.Mock()
        with (
            mock.patch.object(ao.os, "geteuid", return_value=1000),
            mock.patch.object(ao.os, "setgroups", setgroups),
            mock.patch.object(ao.os, "setgid", setgid),
            mock.patch.object(ao.os, "setuid", setuid),
        ):
            ao.drop_privileges(1000, 1000)

        setgroups.assert_not_called()
        setgid.assert_not_called()
        setuid.assert_not_called()

    def test_root_drops_groups_then_gid_then_uid(self) -> None:
        """Privileges are dropped in the correct order."""
        calls = mock.Mock()
        with (
            mock.patch.object(ao.os, "geteuid", return_value=0),
            mock.patch.object(ao.os, "setgroups", calls.setgroups),
            mock.patch.object(ao.os, "setgid", calls.setgid),
            mock.patch.object(ao.os, "setuid", calls.setuid),
        ):
            ao.drop_privileges(1234, 2345)

        assert calls.mock_calls == [
            mock.call.setgroups([]),
            mock.call.setgid(2345),
            mock.call.setuid(1234),
        ]


class ReadIdTests(unittest.TestCase):
    """Test read_id."""

    def test_default_is_used_when_unset(self) -> None:
        """An unset variable falls back to the default ID."""
        with mock.patch.dict(os.environ, {}, clear=True):
            assert ao.read_id("APP_UID", 1000) == 1000

    def test_value_is_parsed(self) -> None:
        """A numeric environment value overrides the default."""
        with mock.patch.dict(os.environ, {"APP_UID": "1001"}, clear=True):
            assert ao.read_id("APP_UID", 1000) == 1001

    def test_whitespace_is_ignored(self) -> None:
        """Surrounding whitespace is stripped before parsing."""
        with mock.patch.dict(os.environ, {"APP_UID": " 1001 "}, clear=True):
            assert ao.read_id("APP_UID", 1000) == 1001

    def test_blank_is_treated_as_unset(self) -> None:
        """An empty value falls back to the default, like the shell default."""
        with mock.patch.dict(os.environ, {"APP_UID": "  "}, clear=True):
            assert ao.read_id("APP_UID", 1000) == 1000

    def test_non_positive_values_are_rejected(self) -> None:
        """Negative IDs and root IDs are rejected."""
        with mock.patch.dict(os.environ, {"APP_UID": "-1"}, clear=True):
            error = assert_raises(ValueError, lambda: ao.read_id("APP_UID", 1000))

        assert "greater than 0" in str(error)

        with mock.patch.dict(os.environ, {"APP_UID": "0"}, clear=True):
            error = assert_raises(ValueError, lambda: ao.read_id("APP_UID", 1000))

        assert "greater than 0" in str(error)

    def test_invalid_value_is_rejected(self) -> None:
        """A non-numeric value gives a clear configuration error."""
        with mock.patch.dict(os.environ, {"APP_UID": "app"}, clear=True):
            error = assert_raises(ValueError, lambda: ao.read_id("APP_UID", 1000))

        assert "APP_UID" in str(error)


class MainTests(unittest.TestCase):
    """Test the main entry point."""

    def test_options_load_error_is_reported(self) -> None:
        """An options read failure returns an error without executing."""
        stderr = io.StringIO()
        with (
            mock.patch.object(ao, "load_options", side_effect=OSError("boom")),
            mock.patch.object(ao, "drop_privileges") as drop,
            mock.patch.object(ao.os, "execve") as execve,
            redirect_stderr(stderr),
        ):
            result = ao.main()

        assert result == 1
        assert "[ERROR] Failed to read add-on options" in stderr.getvalue()
        drop.assert_not_called()
        execve.assert_not_called()

    def test_non_utf8_options_file_is_reported(self) -> None:
        """A non-UTF-8 options file returns a clean error without executing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            options_path = Path(temp_dir) / "options.json"
            options_path.write_bytes(b"\xff")
            stderr = io.StringIO()
            with (
                mock.patch.object(ao, "OPTIONS_PATH", options_path),
                mock.patch.object(ao, "drop_privileges") as drop,
                mock.patch.object(ao.os, "execve") as execve,
                mock.patch.dict(os.environ, {}, clear=True),
                redirect_stdout(io.StringIO()),
                redirect_stderr(stderr),
            ):
                result = ao.main()

        assert result == 1
        assert "[ERROR] Failed to read add-on options" in stderr.getvalue()
        drop.assert_not_called()
        execve.assert_not_called()

    def test_invalid_uid_is_reported(self) -> None:
        """An invalid APP_UID returns an error without executing."""
        stderr = io.StringIO()
        with (
            mock.patch.object(ao, "load_options", return_value={}),
            mock.patch.object(ao, "drop_privileges") as drop,
            mock.patch.object(ao.os, "execve") as execve,
            mock.patch.dict(os.environ, {"APP_UID": "app"}, clear=True),
            redirect_stderr(stderr),
        ):
            result = ao.main()

        assert result == 1
        assert "[ERROR] Invalid app user configuration" in stderr.getvalue()
        drop.assert_not_called()
        execve.assert_not_called()

    def test_invalid_gid_is_reported(self) -> None:
        """An invalid APP_GID returns an error without executing."""
        stderr = io.StringIO()
        with (
            mock.patch.object(ao, "load_options", return_value={}),
            mock.patch.object(ao, "drop_privileges") as drop,
            mock.patch.object(ao.os, "execve") as execve,
            mock.patch.dict(os.environ, {"APP_GID": "-1"}, clear=True),
            redirect_stderr(stderr),
        ):
            result = ao.main()

        assert result == 1
        assert "[ERROR] Invalid app user configuration" in stderr.getvalue()
        drop.assert_not_called()
        execve.assert_not_called()

    def test_invalid_option_value_is_reported(self) -> None:
        """An invalid option value returns an error before dropping privileges."""
        stderr = io.StringIO()
        with (
            mock.patch.object(ao, "load_options", return_value={"stt_engine": ["bad"]}),
            mock.patch.object(ao, "drop_privileges") as drop,
            mock.patch.object(ao.os, "execve") as execve,
            mock.patch.dict(os.environ, {}, clear=True),
            redirect_stderr(stderr),
        ):
            result = ao.main()

        assert result == 1
        assert "[ERROR] Invalid add-on option" in stderr.getvalue()
        drop.assert_not_called()
        execve.assert_not_called()

    def test_drop_privileges_failure_is_reported(self) -> None:
        """A failed privilege drop returns a clean error without executing."""
        stderr = io.StringIO()
        with (
            mock.patch.object(ao, "load_options", return_value={}),
            mock.patch.object(ao, "drop_privileges", side_effect=OSError("boom")),
            mock.patch.object(ao.os, "execve") as execve,
            mock.patch.dict(os.environ, {}, clear=True),
            redirect_stderr(stderr),
        ):
            result = ao.main()

        assert result == 1
        assert "[ERROR] Failed to start Wyoming Vietnamese" in stderr.getvalue()
        execve.assert_not_called()

    def test_exec_failure_is_reported(self) -> None:
        """A failed exec returns a clean error after dropping privileges."""
        stderr = io.StringIO()
        with (
            mock.patch.object(ao, "load_options", return_value={}),
            mock.patch.object(ao, "drop_privileges") as drop,
            mock.patch.object(ao.os, "execve", side_effect=OSError("boom")),
            mock.patch.dict(os.environ, {}, clear=True),
            redirect_stderr(stderr),
        ):
            result = ao.main()

        assert result == 1
        assert "[ERROR] Failed to start Wyoming Vietnamese" in stderr.getvalue()
        drop.assert_called_once_with(1000, 1000)

    def test_success_execs_server_with_environment(self) -> None:
        """A successful run drops privileges and execs the module."""
        with (
            mock.patch.object(
                ao,
                "load_options",
                return_value={"stt_engine": "zipformer", "log_level": "debug"},
            ),
            mock.patch.object(ao, "drop_privileges") as drop,
            mock.patch.object(ao.os, "execve") as execve,
            mock.patch.dict(os.environ, {"EXISTING": "1"}, clear=True),
            redirect_stdout(io.StringIO()),
        ):
            result = ao.main()

        assert result == 0
        drop.assert_called_once_with(1000, 1000)
        execve.assert_called_once()
        call_args = execve.call_args.args
        assert call_args[0] == sys.executable
        assert call_args[1] == [sys.executable, "-m", "wyoming_vietnamese"]
        env = call_args[2]
        assert env["STT_ENGINE"] == "zipformer"
        assert env["LOG_LEVEL"] == "debug"
        assert env["EXISTING"] == "1"
        assert env["HOME"] == "/app"
        assert env["USER"] == "app"
        assert env["LOGNAME"] == "app"

    def test_uid_and_gid_environment_overrides_are_used(self) -> None:
        """APP_UID and APP_GID are passed to the privilege drop."""
        with (
            mock.patch.object(ao, "load_options", return_value={}),
            mock.patch.object(ao, "drop_privileges") as drop,
            mock.patch.object(ao.os, "execve"),
            mock.patch.dict(
                os.environ,
                {"APP_UID": "1234", "APP_GID": "2345"},
                clear=True,
            ),
            redirect_stdout(io.StringIO()),
        ):
            result = ao.main()

        assert result == 0
        drop.assert_called_once_with(1234, 2345)

    def test_missing_options_file_continues_with_defaults(self) -> None:
        """A missing options file warns but still starts the server."""
        with tempfile.TemporaryDirectory() as temp_dir:
            options_path = Path(temp_dir) / "missing.json"
            stdout = io.StringIO()
            with (
                mock.patch.object(ao, "OPTIONS_PATH", options_path),
                mock.patch.object(ao, "drop_privileges"),
                mock.patch.object(ao.os, "execve") as execve,
                mock.patch.dict(os.environ, {}, clear=True),
                redirect_stdout(stdout),
            ):
                result = ao.main()

            assert result == 0
            assert "[WARN] Options file not found" in stdout.getvalue()
            env = execve.call_args.args[2]
            assert "STT_ENGINE" not in env

    def test_options_file_is_read_and_applied(self) -> None:
        """A real options file is translated into the server environment."""
        with tempfile.TemporaryDirectory() as temp_dir:
            options_path = Path(temp_dir) / "options.json"
            options_path.write_text(
                '{"stt_engine": "gipformer", "tts_voice": "voice"}',
                encoding="utf-8",
            )
            with (
                mock.patch.object(ao, "OPTIONS_PATH", options_path),
                mock.patch.object(ao, "drop_privileges"),
                mock.patch.object(ao.os, "execve") as execve,
                mock.patch.dict(os.environ, {}, clear=True),
                redirect_stdout(io.StringIO()),
            ):
                result = ao.main()

            assert result == 0
            env = execve.call_args.args[2]
            assert env["STT_ENGINE"] == "gipformer"
            assert env["TTS_VOICE"] == "voice"


class EntryPointTests(unittest.TestCase):
    """Test the module entry point."""

    def test_module_entry_point_exits_with_main_result(self) -> None:
        """Running the script exits with main's return code after exec."""
        with (
            mock.patch.object(os, "geteuid", return_value=1000),
            mock.patch.object(os, "execve") as execve,
            mock.patch.object(Path, "exists", return_value=False),
            mock.patch.dict(os.environ, {}, clear=True),
            redirect_stdout(io.StringIO()),
        ):
            error = assert_raises(
                SystemExit,
                lambda: runpy.run_path(str(SCRIPT), run_name="__main__"),
            )

        assert isinstance(error, SystemExit)
        assert error.code == 0
        execve.assert_called_once()


if __name__ == "__main__":
    unittest.main()
