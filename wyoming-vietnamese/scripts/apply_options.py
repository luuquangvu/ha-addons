"""Translate Home Assistant add-on options into the server's environment variables."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

OPTIONS_PATH = Path("/data/options.json")
PROGRAM_MODULE = "wyoming_vietnamese"

# Add-on option name -> environment variable read by wyoming_vietnamese.config.
OPTION_ENV_NAMES: dict[str, str] = {
    "tts_voice": "TTS_VOICE",
    "cpu_threads": "CPU_THREADS",
    "offline": "OFFLINE",
    "tts_sentence_silence_ms": "TTS_SENTENCE_SILENCE_MS",
    "tts_clause_silence_ms": "TTS_CLAUSE_SILENCE_MS",
    "tts_silence_jitter_percent": "TTS_SILENCE_JITTER_PERCENT",
    "log_level": "LOG_LEVEL",
}


def load_options(path: Path) -> dict[str, Any]:
    """Read the add-on options file, tolerating a missing or empty file."""
    if not path.exists():
        print(f"[WARN] Options file not found: {path}; using defaults.")
        return {}

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

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


def main() -> int:
    """Apply the add-on options and hand the process over to the server."""
    try:
        options = load_options(OPTIONS_PATH)
    except (OSError, TypeError, json.JSONDecodeError) as error:
        print(f"[ERROR] Failed to read add-on options: {error}", file=sys.stderr)
        return 1

    env = build_environment(options)
    os.execve(sys.executable, [sys.executable, "-m", PROGRAM_MODULE], env)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
