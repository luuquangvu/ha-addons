"""Translate Home Assistant add-on options into the server's environment variables."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

OPTIONS_PATH = Path("/data/options.json")
PROGRAM_MODULE = "wyoming_vietnamese"
DEFAULT_APP_UID = 1000
DEFAULT_APP_GID = 1000
APP_HOME = "/app"

# Add-on option name -> environment variable read by wyoming_vietnamese.config.
OPTION_ENV_NAMES: dict[str, str] = {
    "stt_engine": "STT_ENGINE",
    "tts_engine": "TTS_ENGINE",
    "tts_voice": "TTS_VOICE",
    "log_level": "LOG_LEVEL",
}


def load_options(path: Path) -> dict[str, Any]:
    """Read the add-on options file, tolerating a missing or empty file."""
    if not path.exists():
        print(f"[WARN] Options file not found: {path}; using defaults.")
        return {}

    with path.open("r", encoding="utf-8") as file:
        content = file.read()

    if not content.strip():
        print(f"[WARN] Options file is empty: {path}; using defaults.")
        return {}

    data = json.loads(content)

    if not isinstance(data, dict):
        raise TypeError(f"{path} must contain a JSON object")

    return data


def format_value(value: Any) -> str | None:
    """Render one option as an environment value, or None when it carries no setting."""
    if value is None:
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int | float | str):
        text = str(value).strip()
        return text or None

    raise ValueError(f"Unsupported option value type: {type(value).__name__}")


def build_environment(options: dict[str, Any]) -> dict[str, str]:
    """Overlay the configured options onto the container environment."""
    env = dict(os.environ)

    for option_name, env_name in OPTION_ENV_NAMES.items():
        if option_name not in options:
            continue

        value = format_value(options[option_name])
        if value is None:
            continue

        env[env_name] = value
        print(f"[INFO] {env_name}={value}")

    return env


def drop_privileges(uid: int, gid: int) -> None:
    """Drop root privileges before handing over to the unprivileged server."""
    if os.geteuid() != 0:
        return

    os.setgroups([])
    os.setgid(gid)
    os.setuid(uid)


def read_id(name: str, default: int) -> int:
    """Read a positive numeric ID from the environment."""
    raw_value = os.environ.get(name)
    if raw_value is None or not raw_value.strip():
        return default

    raw_value = raw_value.strip()
    try:
        value = int(raw_value)
    except ValueError as error:
        raise ValueError(f"{name} must be an integer, got {raw_value!r}") from error

    if value <= 0:
        raise ValueError(f"{name} must be greater than 0, got {value}")

    return value


def main() -> int:
    """Apply the add-on options and hand the process over to the server."""
    try:
        options = load_options(OPTIONS_PATH)
    except (OSError, TypeError, UnicodeError, json.JSONDecodeError) as error:
        print(f"[ERROR] Failed to read add-on options: {error}", file=sys.stderr)
        return 1

    try:
        app_uid = read_id("APP_UID", DEFAULT_APP_UID)
        app_gid = read_id("APP_GID", DEFAULT_APP_GID)
    except ValueError as error:
        print(f"[ERROR] Invalid app user configuration: {error}", file=sys.stderr)
        return 1

    try:
        env = build_environment(options)
    except ValueError as error:
        print(f"[ERROR] Invalid add-on option: {error}", file=sys.stderr)
        return 1

    env["HOME"] = APP_HOME
    env["USER"] = "app"
    env["LOGNAME"] = "app"

    try:
        drop_privileges(app_uid, app_gid)
        os.execve(sys.executable, [sys.executable, "-m", PROGRAM_MODULE], env)
    except (OSError, ValueError) as error:
        print(f"[ERROR] Failed to start Wyoming Vietnamese: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
