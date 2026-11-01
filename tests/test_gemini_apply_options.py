"""Full regression tests for the Gemini FastAPI options bridge."""

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

SCRIPT = Path(__file__).resolve().parents[1] / "gemini-fastapi" / "scripts" / "apply_options.py"


def load_module() -> ModuleType:
    """Load apply_options.py without importing the hyphenated add-on directory."""
    spec = importlib.util.spec_from_file_location("gemini_apply_options", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {SCRIPT}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ap = load_module()


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


def client(
    *,
    client_id: str = "",
    secure_1psid: str = "psid",
    secure_1psidts: str = "psidts",
    proxy: str = "",
) -> dict[str, str]:
    """Return one add-on client option mapping."""
    return {
        "id": client_id,
        "secure_1psid": secure_1psid,
        "secure_1psidts": secure_1psidts,
        "proxy": proxy,
    }


class LoadOptionsTests(unittest.TestCase):
    """Test load_options."""

    def test_missing_file_returns_empty_options(self) -> None:
        """A missing options file falls back to an empty mapping."""
        with tempfile.TemporaryDirectory() as temp_dir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                result = ap.load_options(Path(temp_dir) / "missing.json")

        assert result == {}
        assert "[WARN] Options file not found" in stdout.getvalue()

    def test_empty_file_returns_empty_options(self) -> None:
        """An empty options file falls back to an empty mapping."""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "options.json"
            path.write_text("", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                result = ap.load_options(path)

        assert result == {}
        assert "[WARN] Options file is empty" in stdout.getvalue()

    def test_valid_object_is_loaded(self) -> None:
        """A JSON object is returned as a dictionary."""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "options.json"
            path.write_text('{"api_key": "secret"}', encoding="utf-8")

            result = ap.load_options(path)

        assert result == {"api_key": "secret"}

    def test_non_object_is_rejected(self) -> None:
        """A JSON value other than an object is rejected."""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "options.json"
            path.write_text("[]", encoding="utf-8")

            error = assert_raises(TypeError, lambda: ap.load_options(path))

        assert "must contain a JSON object" in str(error)

    def test_invalid_json_is_rejected(self) -> None:
        """Malformed JSON propagates a JSONDecodeError."""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "options.json"
            path.write_text("{", encoding="utf-8")

            assert_raises(json.JSONDecodeError, lambda: ap.load_options(path))

    def test_os_error_is_propagated(self) -> None:
        """An unreadable path propagates an OSError."""
        with tempfile.TemporaryDirectory() as temp_dir:
            assert_raises(OSError, lambda: ap.load_options(Path(temp_dir)))


class FormatValueTests(unittest.TestCase):
    """Test format_value."""

    def test_none_is_unset(self) -> None:
        """None carries no setting."""
        assert ap.format_value(None) is None

    def test_booleans_use_lowercase(self) -> None:
        """Booleans become lowercase strings."""
        assert ap.format_value(True) == "true"
        assert ap.format_value(False) == "false"

    def test_numbers_are_converted(self) -> None:
        """Integer and float values become strings."""
        assert ap.format_value(0) == "0"
        assert ap.format_value(-1) == "-1"
        assert ap.format_value(1.5) == "1.5"

    def test_strings_are_stripped(self) -> None:
        """Surrounding whitespace is removed."""
        assert ap.format_value(" value ") == "value"

    def test_empty_strings_are_unset(self) -> None:
        """Empty and whitespace-only strings carry no setting."""
        assert ap.format_value("") is None
        assert ap.format_value("   ") is None

    def test_unsupported_types_are_rejected(self) -> None:
        """Lists and mappings are rejected."""
        assert_raises(ValueError, lambda: ap.format_value(["value"]))
        assert_raises(ValueError, lambda: ap.format_value({"value": 1}))


class NormalizeValueTests(unittest.TestCase):
    """Test normalize_value."""

    def test_log_level_is_uppercased(self) -> None:
        """The log level matches Gemini FastAPI's uppercase literal values."""
        assert ap.normalize_value("log_level", "debug") == "DEBUG"

    def test_other_options_are_unchanged(self) -> None:
        """Secrets keep their original casing."""
        assert ap.normalize_value("api_key", "MiXeD") == "MiXeD"


class ClientHelperTests(unittest.TestCase):
    """Test client helper functions."""

    def test_default_client_id_is_derived_from_the_cookie(self) -> None:
        """The default ID ignores cookie rotation and stays stable."""
        account = client(secure_1psid="psid", secure_1psidts="psidts")
        same_account = client(secure_1psid="psid", secure_1psidts="rotated")
        other_account = client(secure_1psid="psid-2")

        assert ap.default_client_id(account) == ap.default_client_id(same_account)
        assert ap.default_client_id(account) != ap.default_client_id(other_account)
        assert ap.default_client_id(account).startswith("client-")

    def test_complete_cookie_pair_is_authenticated(self) -> None:
        """Both required cookies mark a client as authenticated."""
        assert ap.validate_client_cookies(client(), 0)

    def test_missing_secure_1psidts_is_rejected(self) -> None:
        """A 1PSID without 1PSIDTS cannot sign in."""
        error = assert_raises(
            ValueError,
            lambda: ap.validate_client_cookies(
                client(secure_1psid="psid", secure_1psidts=""),
                2,
            ),
        )

        assert "clients[2].secure_1psidts" in str(error)
        assert "required" in str(error)

    def test_missing_secure_1psid_is_rejected(self) -> None:
        """A 1PSIDTS without 1PSID cannot sign in."""
        error = assert_raises(
            ValueError,
            lambda: ap.validate_client_cookies(
                client(secure_1psid="", secure_1psidts="psidts"),
                1,
            ),
        )

        assert "clients[1].secure_1psid" in str(error)
        assert "required" in str(error)

    def test_client_without_cookies_is_a_guest(self) -> None:
        """An entry with neither cookie is a guest client."""
        assert not ap.validate_client_cookies(client(secure_1psid="", secure_1psidts=""), 0)
        assert not ap.validate_client_cookies(client(secure_1psid="  ", secure_1psidts="\t"), 0)


class RedactProxyTests(unittest.TestCase):
    """Test proxy log redaction."""

    def test_proxy_without_credentials_is_unchanged(self) -> None:
        """A plain proxy URL is logged as-is."""
        assert ap.redact_proxy("socks5://127.0.0.1:1080") == "socks5://127.0.0.1:1080"

    def test_proxy_with_credentials_is_masked(self) -> None:
        """User information is replaced with a mask."""
        assert (
            ap.redact_proxy("socks5://user:secret@127.0.0.1:1080") == "socks5://***@127.0.0.1:1080"
        )
        assert ap.redact_proxy("user:secret@127.0.0.1:1080") == "***@127.0.0.1:1080"


class ApplyClientsTests(unittest.TestCase):
    """Test apply_clients."""

    def test_clients_are_mapped_in_order(self) -> None:
        """Each configured client maps to a contiguous upstream index."""
        env: dict[str, str] = {}
        first = client(proxy="")
        second = client(secure_1psid="psid-2", secure_1psidts="psidts-2")
        with redirect_stdout(io.StringIO()):
            ap.apply_clients(env, [first, second])

        assert env["CONFIG_GEMINI__CLIENTS__0__ID"] == ap.default_client_id(first)
        assert env["CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID"] == "psid"
        assert env["CONFIG_GEMINI__CLIENTS__1__ID"] == ap.default_client_id(second)
        assert env["CONFIG_GEMINI__CLIENTS__1__SECURE_1PSID"] == "psid-2"
        assert env["CONFIG_GEMINI__CLIENTS__1__SECURE_1PSIDTS"] == "psidts-2"

    def test_blank_clients_are_skipped_without_shifting_ids(self) -> None:
        """Empty entries do not leave gaps but keep the account-derived ID."""
        env: dict[str, str] = {}
        second = client(secure_1psid="psid-2", secure_1psidts="psidts-2")
        with redirect_stdout(io.StringIO()):
            ap.apply_clients(
                env,
                [
                    client(secure_1psid="", secure_1psidts=""),
                    second,
                ],
            )

        assert env["CONFIG_GEMINI__CLIENTS__0__ID"] == ap.default_client_id(second)
        assert env["CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID"] == "psid-2"
        assert "CONFIG_GEMINI__CLIENTS__1__ID" not in env

    def test_removing_an_earlier_client_keeps_later_ids(self) -> None:
        """A later account keeps its ID when an earlier entry is removed."""
        before: dict[str, str] = {}
        after: dict[str, str] = {}
        first = client(secure_1psid="psid-1", secure_1psidts="psidts-1")
        second = client(secure_1psid="psid-2", secure_1psidts="psidts-2")
        with redirect_stdout(io.StringIO()):
            ap.apply_clients(before, [first, second])
            ap.apply_clients(after, [second])

        assert before["CONFIG_GEMINI__CLIENTS__1__ID"] == after["CONFIG_GEMINI__CLIENTS__0__ID"]

    def test_blank_optional_fields_are_emitted_as_empty_values(self) -> None:
        """Blank fields override the placeholder client shipped upstream."""
        env: dict[str, str] = {}
        with redirect_stdout(io.StringIO()):
            ap.apply_clients(env, [client(proxy="")])

        assert env["CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID"] == "psid"
        assert env["CONFIG_GEMINI__CLIENTS__0__SECURE_1PSIDTS"] == "psidts"
        assert env["CONFIG_GEMINI__CLIENTS__0__PROXY"] == ""
        assert "CONFIG_GEMINI__CLIENTS__0__IMPERSONATE" not in env

    def test_proxy_credentials_are_masked_in_the_log(self) -> None:
        """Proxy user information is not written to the startup log."""
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            ap.apply_clients(
                {},
                [client(proxy="socks5://proxy-user:proxy-secret@127.0.0.1:1080")],
            )

        output = stdout.getvalue()
        assert "proxy-user" not in output
        assert "proxy-secret" not in output
        assert "socks5://***@127.0.0.1:1080" in output

    def test_explicit_id_and_optional_client_fields_are_used(self) -> None:
        """An explicit ID and proxy override the defaults."""
        env: dict[str, str] = {}
        with redirect_stdout(io.StringIO()):
            ap.apply_clients(
                env,
                [
                    {
                        **client(
                            client_id="main",
                            proxy="socks5://127.0.0.1:1080",
                        ),
                        "impersonate": "chrome",
                    }
                ],
            )

        assert env["CONFIG_GEMINI__CLIENTS__0__ID"] == "main"
        assert env["CONFIG_GEMINI__CLIENTS__0__PROXY"] == "socks5://127.0.0.1:1080"
        assert "CONFIG_GEMINI__CLIENTS__0__IMPERSONATE" not in env

    def test_client_secrets_are_masked_in_the_log(self) -> None:
        """Cookie values are not printed at startup."""
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            ap.apply_clients({}, [client()])

        output = stdout.getvalue()
        assert "psid" not in output
        assert "psidts" not in output
        assert "CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID=***" in output

    def test_clients_must_be_a_list(self) -> None:
        """A non-list clients option is rejected."""
        error = assert_raises(ValueError, lambda: ap.apply_clients({}, {"id": "main"}))

        assert "clients must be a list" in str(error)

    def test_client_entries_must_be_objects(self) -> None:
        """A client list item must be a mapping."""
        error = assert_raises(ValueError, lambda: ap.apply_clients({}, ["cookie"]))

        assert "clients[0] must be an object" in str(error)

    def test_duplicate_client_ids_are_rejected(self) -> None:
        """Duplicate explicit client IDs are rejected."""
        error = assert_raises(
            ValueError,
            lambda: ap.apply_clients({}, [client(client_id="main"), client(client_id="main")]),
        )

        assert "Duplicate Gemini client ID" in str(error)

    def test_duplicate_accounts_are_rejected(self) -> None:
        """The same account cannot be added twice without explicit IDs."""
        error = assert_raises(
            ValueError,
            lambda: ap.apply_clients(
                {},
                [client(secure_1psid="psid"), client(secure_1psid="psid", proxy="socks5://x")],
            ),
        )

        assert "Duplicate Gemini client ID" in str(error)

    def test_no_clients_adds_one_guest_client(self) -> None:
        """A missing clients option starts one guest client."""
        env: dict[str, str] = {}
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            account_count = ap.apply_clients(env, None)

        assert account_count == 0
        assert env["CONFIG_GEMINI__CLIENTS__0__ID"] == ap.GUEST_CLIENT_ID
        assert env["CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID"] == ""
        assert env["CONFIG_GEMINI__CLIENTS__0__SECURE_1PSIDTS"] == ""
        assert "guest mode" in stdout.getvalue()

    def test_blank_entries_start_one_guest_client(self) -> None:
        """All-empty account entries collapse to a single guest client."""
        env: dict[str, str] = {}
        with redirect_stdout(io.StringIO()):
            account_count = ap.apply_clients(
                env,
                [
                    client(secure_1psid="", secure_1psidts=""),
                    client(secure_1psid=" ", secure_1psidts="\t"),
                ],
            )

        assert account_count == 0
        assert env["CONFIG_GEMINI__CLIENTS__0__ID"] == ap.GUEST_CLIENT_ID
        assert "CONFIG_GEMINI__CLIENTS__1__ID" not in env

    def test_accounts_are_counted(self) -> None:
        """The returned count reflects only authenticated accounts."""
        with redirect_stdout(io.StringIO()):
            account_count = ap.apply_clients(
                {},
                [client(secure_1psid="psid-1"), client(secure_1psid="psid-2")],
            )

        assert account_count == 2

    def test_incomplete_cookie_pair_is_rejected(self) -> None:
        """A half-configured account fails instead of silently becoming a guest."""
        error = assert_raises(
            ValueError,
            lambda: ap.apply_clients({}, [client(secure_1psidts="")]),
        )

        assert "clients[0].secure_1psidts" in str(error)


class BuildEnvironmentTests(unittest.TestCase):
    """Test build_environment."""

    def test_top_level_options_are_mapped(self) -> None:
        """API key and log level map to their server environment variables."""
        stdout = io.StringIO()
        with (
            mock.patch.dict(os.environ, {"EXISTING": "1"}, clear=True),
            redirect_stdout(stdout),
        ):
            env = ap.build_environment({"api_key": "secret", "log_level": "debug"})

        assert env["CONFIG_SERVER__API_KEY"] == "secret"
        assert env["CONFIG_LOGGING__LEVEL"] == "DEBUG"
        assert env["EXISTING"] == "1"
        assert "[INFO] CONFIG_LOGGING__LEVEL=DEBUG" in stdout.getvalue()

    def test_secret_values_are_not_printed(self) -> None:
        """Secret option values are masked in the startup log."""
        stdout = io.StringIO()
        with (
            mock.patch.dict(os.environ, {}, clear=True),
            redirect_stdout(stdout),
        ):
            ap.build_environment({"api_key": "secret"})

        output = stdout.getvalue()
        assert "secret" not in output
        assert "[INFO] CONFIG_SERVER__API_KEY=***" in output

    def test_missing_options_are_skipped(self) -> None:
        """Options absent from the file do not create environment variables."""
        with (
            mock.patch.dict(os.environ, {}, clear=True),
            redirect_stdout(io.StringIO()),
        ):
            env = ap.build_environment({"api_key": "secret"})

        assert env["CONFIG_SERVER__API_KEY"] == "secret"
        assert "CONFIG_LOGGING__LEVEL" not in env
        assert env["CONFIG_GEMINI__CLIENTS__0__ID"] == ap.GUEST_CLIENT_ID
        assert env["CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID"] == ""

    def test_unset_values_are_skipped(self) -> None:
        """None and blank option values do not override the environment."""
        with (
            mock.patch.dict(os.environ, {"CONFIG_SERVER__API_KEY": "existing"}, clear=True),
            redirect_stdout(io.StringIO()),
        ):
            env = ap.build_environment({"api_key": None, "log_level": "   "})

        assert env["CONFIG_SERVER__API_KEY"] == "existing"
        assert "CONFIG_LOGGING__LEVEL" not in env

    def test_values_override_existing_environment(self) -> None:
        """Configured options replace inherited environment values."""
        with (
            mock.patch.dict(os.environ, {"CONFIG_LOGGING__LEVEL": "INFO"}, clear=True),
            redirect_stdout(io.StringIO()),
        ):
            env = ap.build_environment({"log_level": "warning"})

        assert env["CONFIG_LOGGING__LEVEL"] == "WARNING"

    def test_unknown_options_are_ignored(self) -> None:
        """Options not in the mapping are ignored."""
        with (
            mock.patch.dict(os.environ, {}, clear=True),
            redirect_stdout(io.StringIO()),
        ):
            env = ap.build_environment({"unknown": "value"})

        assert "unknown" not in env
        assert "UNKNOWN" not in env

    def test_boolean_and_numeric_values_are_formatted(self) -> None:
        """Non-string option values are formatted before use."""
        with (
            mock.patch.dict(os.environ, {}, clear=True),
            redirect_stdout(io.StringIO()),
        ):
            env = ap.build_environment({"api_key": True, "log_level": 3})

        assert env["CONFIG_SERVER__API_KEY"] == "true"
        assert env["CONFIG_LOGGING__LEVEL"] == "3"

    def test_unsupported_option_value_raises(self) -> None:
        """An unsupported option type is not silently accepted."""
        with mock.patch.dict(os.environ, {}, clear=True):
            assert_raises(
                ValueError,
                lambda: ap.build_environment({"api_key": ["value"]}),
            )

    def test_clients_are_applied_from_options(self) -> None:
        """The clients option is translated into upstream client variables."""
        options = {
            "clients": [
                client(),
                client(secure_1psid="psid-2", secure_1psidts="psidts-2"),
            ]
        }
        with (
            mock.patch.dict(os.environ, {}, clear=True),
            redirect_stdout(io.StringIO()),
        ):
            env = ap.build_environment(options)

        assert env["CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID"] == "psid"
        assert env["CONFIG_GEMINI__CLIENTS__1__SECURE_1PSID"] == "psid-2"

    def test_guest_mode_uses_a_fresh_cookie_cache(self) -> None:
        """Guest mode cannot reuse cookies cached for a removed account."""
        with (
            mock.patch.dict(os.environ, {"GEMINI_COOKIE_PATH": "/data/cache"}, clear=True),
            redirect_stdout(io.StringIO()),
        ):
            env = ap.build_environment({})

        assert env["GEMINI_COOKIE_PATH"].startswith(ap.GUEST_COOKIE_PATH_PREFIX)
        assert env["GEMINI_COOKIE_PATH"] != "/data/cache"

    def test_account_mode_keeps_the_configured_cookie_cache(self) -> None:
        """A configured account keeps the persistent cookie cache path."""
        with (
            mock.patch.dict(os.environ, {"GEMINI_COOKIE_PATH": "/data/cache"}, clear=True),
            redirect_stdout(io.StringIO()),
        ):
            env = ap.build_environment({"clients": [client()]})

        assert env["GEMINI_COOKIE_PATH"] == "/data/cache"


class MainTests(unittest.TestCase):
    """Test the main entry point."""

    def test_options_load_error_is_reported(self) -> None:
        """An options read failure returns an error without executing."""
        stderr = io.StringIO()
        with (
            mock.patch.object(ap, "load_options", side_effect=OSError("boom")),
            mock.patch.object(ap.os, "execve") as execve,
            redirect_stderr(stderr),
        ):
            result = ap.main()

        assert result == 1
        assert "[ERROR] Failed to read add-on options" in stderr.getvalue()
        execve.assert_not_called()

    def test_invalid_option_is_reported(self) -> None:
        """An invalid option value returns an error without executing."""
        stderr = io.StringIO()
        with (
            mock.patch.object(ap, "load_options", return_value={"api_key": ["value"]}),
            mock.patch.object(ap.os, "execve") as execve,
            redirect_stderr(stderr),
        ):
            result = ap.main()

        assert result == 1
        assert "[ERROR] Invalid add-on option" in stderr.getvalue()
        execve.assert_not_called()

    def test_non_utf8_options_file_is_reported(self) -> None:
        """A non-UTF-8 options file returns a clean error without executing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            options_path = Path(temp_dir) / "options.json"
            options_path.write_bytes(b"\xff")
            stderr = io.StringIO()
            with (
                mock.patch.object(ap, "OPTIONS_PATH", options_path),
                mock.patch.object(ap.os, "execve") as execve,
                redirect_stdout(io.StringIO()),
                redirect_stderr(stderr),
            ):
                result = ap.main()

        assert result == 1
        assert "[ERROR] Failed to read add-on options" in stderr.getvalue()
        execve.assert_not_called()

    def test_exec_failure_is_reported(self) -> None:
        """A failure to replace the process returns a clean error."""
        stderr = io.StringIO()
        with (
            mock.patch.object(ap, "load_options", return_value={"clients": [client()]}),
            mock.patch.object(ap.os, "execve", side_effect=OSError("boom")),
            mock.patch.dict(os.environ, {}, clear=True),
            redirect_stdout(io.StringIO()),
            redirect_stderr(stderr),
        ):
            result = ap.main()

        assert result == 1
        assert "[ERROR] Failed to start Gemini FastAPI" in stderr.getvalue()

    def test_success_execs_server_with_environment(self) -> None:
        """A successful run execs the upstream entry point."""
        options = {
            "api_key": "secret",
            "log_level": "debug",
            "clients": [
                client(client_id="main"),
                client(
                    client_id="backup",
                    secure_1psid="psid-2",
                    secure_1psidts="psidts-2",
                ),
            ],
        }
        with (
            mock.patch.object(ap, "load_options", return_value=options),
            mock.patch.object(ap.os, "execve") as execve,
            mock.patch.dict(os.environ, {"EXISTING": "1"}, clear=True),
            redirect_stdout(io.StringIO()),
        ):
            result = ap.main()

        assert result == 0
        execve.assert_called_once()
        call_args = execve.call_args.args
        assert call_args[0] == sys.executable
        assert call_args[1] == [sys.executable, "/app/run.py"]
        env = call_args[2]
        assert env["CONFIG_SERVER__API_KEY"] == "secret"
        assert env["CONFIG_LOGGING__LEVEL"] == "DEBUG"
        assert env["CONFIG_GEMINI__CLIENTS__0__ID"] == "main"
        assert env["CONFIG_GEMINI__CLIENTS__1__ID"] == "backup"
        assert env["CONFIG_GEMINI__CLIENTS__1__SECURE_1PSID"] == "psid-2"
        assert env["EXISTING"] == "1"

    def test_missing_options_file_starts_in_guest_mode(self) -> None:
        """A missing options file starts the server with one guest client."""
        with tempfile.TemporaryDirectory() as temp_dir:
            options_path = Path(temp_dir) / "missing.json"
            stdout = io.StringIO()
            with (
                mock.patch.object(ap, "OPTIONS_PATH", options_path),
                mock.patch.object(ap.os, "execve") as execve,
                mock.patch.dict(os.environ, {}, clear=True),
                redirect_stdout(stdout),
            ):
                result = ap.main()

            assert result == 0
            assert "[WARN] Options file not found" in stdout.getvalue()
            assert "guest mode" in stdout.getvalue()
            env = execve.call_args.args[2]
            assert env["CONFIG_GEMINI__CLIENTS__0__ID"] == ap.GUEST_CLIENT_ID

    def test_blank_clients_start_in_guest_mode(self) -> None:
        """An all-empty account list starts the server in guest mode."""
        options = {"clients": [client(secure_1psid="", secure_1psidts="")]}
        stdout = io.StringIO()
        with (
            mock.patch.object(ap, "load_options", return_value=options),
            mock.patch.object(ap.os, "execve") as execve,
            mock.patch.dict(os.environ, {}, clear=True),
            redirect_stdout(stdout),
        ):
            result = ap.main()

        assert result == 0
        assert "guest mode" in stdout.getvalue()
        env = execve.call_args.args[2]
        assert env["CONFIG_GEMINI__CLIENTS__0__ID"] == ap.GUEST_CLIENT_ID

    def test_incomplete_cookie_pair_is_reported(self) -> None:
        """An account with only one cookie fails with a clear error."""
        options = {"clients": [client(secure_1psid="psid", secure_1psidts="")]}
        stderr = io.StringIO()
        with (
            mock.patch.object(ap, "load_options", return_value=options),
            mock.patch.object(ap.os, "execve") as execve,
            mock.patch.dict(os.environ, {}, clear=True),
            redirect_stdout(io.StringIO()),
            redirect_stderr(stderr),
        ):
            result = ap.main()

        assert result == 1
        assert "[ERROR] Invalid add-on option" in stderr.getvalue()
        assert "clients[0].secure_1psidts" in stderr.getvalue()
        execve.assert_not_called()

    def test_options_file_is_read_and_applied(self) -> None:
        """A real options file is translated into the server environment."""
        with tempfile.TemporaryDirectory() as temp_dir:
            options_path = Path(temp_dir) / "options.json"
            options_path.write_text(
                '{"log_level": "info", "clients": ['
                '{"secure_1psid": "psid", "secure_1psidts": "psidts"}]}',
                encoding="utf-8",
            )
            with (
                mock.patch.object(ap, "OPTIONS_PATH", options_path),
                mock.patch.object(ap.os, "execve") as execve,
                mock.patch.dict(os.environ, {}, clear=True),
                redirect_stdout(io.StringIO()),
            ):
                result = ap.main()

            assert result == 0
            env = execve.call_args.args[2]
            assert env["CONFIG_LOGGING__LEVEL"] == "INFO"
            assert env["CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID"] == "psid"


class EntryPointTests(unittest.TestCase):
    """Test the module entry point."""

    def test_module_entry_point_exits_with_main_result(self) -> None:
        """Running the script with no options starts guest mode and exits 0."""
        with (
            mock.patch.object(ap.os, "execve") as execve,
            mock.patch.object(Path, "exists", return_value=False),
            mock.patch.dict(os.environ, {}, clear=True),
            redirect_stdout(io.StringIO()),
            redirect_stderr(io.StringIO()),
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
