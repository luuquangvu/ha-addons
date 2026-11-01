"""Apply Home Assistant add-on options to the Gemini FastAPI environment."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

OPTIONS_PATH = Path("/data/options.json")
RUN_SCRIPT = "/app/run.py"

# Add-on option name -> environment variable read by Gemini FastAPI's config.
# The upstream default config/config.yaml stays untouched; these values override it.
OPTION_ENV_NAMES: dict[str, str] = {
    "api_key": "CONFIG_SERVER__API_KEY",
    "log_level": "CONFIG_LOGGING__LEVEL",
}

CLIENT_ENV_PREFIX = "CONFIG_GEMINI__CLIENTS__"
CLIENT_FIELDS: dict[str, str] = {
    "id": "ID",
    "secure_1psid": "SECURE_1PSID",
    "secure_1psidts": "SECURE_1PSIDTS",
    "proxy": "PROXY",
}
SECRET_FIELDS = frozenset({"api_key", "secure_1psid", "secure_1psidts"})
UPPERCASE_OPTIONS = frozenset({"log_level"})
GUEST_CLIENT_ID = "guest"
GUEST_COOKIE_PATH_PREFIX = "/tmp/gemini-fastapi-guest-cache"


def load_options(path: Path) -> dict[str, Any]:
    """Read the add-on options file, tolerating a missing or empty file."""
    if not path.exists():
        print(f"[WARN] Options file not found: {path}.")
        return {}

    with path.open("r", encoding="utf-8") as file:
        content = file.read()

    if not content.strip():
        print(f"[WARN] Options file is empty: {path}.")
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


def normalize_value(option_name: str, value: str) -> str:
    """Normalize a formatted option for the environment variable it targets."""
    return value.upper() if option_name in UPPERCASE_OPTIONS else value


def redact_proxy(value: str) -> str:
    """Hide any credentials embedded in a proxy URL before logging it."""
    if "@" not in value:
        return value

    host = value.rpartition("@")[2]
    scheme, separator, _ = value.partition("://")
    return f"{scheme}://***@{host}" if separator else f"***@{host}"


def default_client_id(client: dict[str, Any]) -> str:
    """Return a stable client ID derived from the account's required cookie.

    Deriving the ID from __Secure-1PSID keeps it stable when the account list
    is reordered, when entries are removed, or when a previously empty entry is
    filled. Users can still set an explicit readable ID in the options.
    """
    psid = format_value(client.get("secure_1psid")) or ""
    digest = hashlib.sha256(psid.encode("utf-8")).hexdigest()
    return f"client-{digest[:12]}"


def validate_client_cookies(client: dict[str, Any], position: int) -> bool:
    """Validate one client's cookie pair and return whether it is authenticated.

    Gemini FastAPI needs both __Secure-1PSID and __Secure-1PSIDTS to sign in.
    An entry with only one of them cannot authenticate and is rejected instead
    of silently running as a guest. An entry with neither cookie is a guest
    client: it can answer text prompts but has no history, uploads, or model
    choice.
    """
    secure_1psid = format_value(client.get("secure_1psid"))
    secure_1psidts = format_value(client.get("secure_1psidts"))

    if secure_1psid is not None and secure_1psidts is None:
        raise ValueError(f"clients[{position}].secure_1psidts is required when secure_1psid is set")
    if secure_1psidts is not None and secure_1psid is None:
        raise ValueError(f"clients[{position}].secure_1psid is required when secure_1psidts is set")

    return secure_1psid is not None and secure_1psidts is not None


def display_client_value(field: str, value: str) -> str:
    """Return a log-safe rendering of one client field value."""
    if field in SECRET_FIELDS:
        return "***" if value else ""
    return redact_proxy(value) if field == "proxy" else value


def add_client_environment(
    env: dict[str, str],
    index: int,
    client_id: str,
    client: dict[str, Any],
) -> None:
    """Write one indexed client block, overriding the upstream placeholder client."""
    for field, suffix in CLIENT_FIELDS.items():
        field_value = client_id if field == "id" else format_value(client.get(field)) or ""

        env_name = f"{CLIENT_ENV_PREFIX}{index}__{suffix}"
        env[env_name] = field_value
        print(f"[INFO] {env_name}={display_client_value(field, field_value)}")


def apply_clients(env: dict[str, str], clients: Any) -> int:
    """Add one environment block per account and return the account count.

    Upstream always needs at least one client, so when no account is
    configured a single guest client is added instead of failing startup.
    """
    if clients is None:
        clients = []
    if not isinstance(clients, list):
        raise ValueError("clients must be a list")

    used_ids: set[str] = set()
    env_index = 0

    for position, value in enumerate(clients):
        if not isinstance(value, dict):
            raise ValueError(f"clients[{position}] must be an object")

        client: dict[str, Any] = value
        if not validate_client_cookies(client, position):
            continue

        client_id = format_value(client.get("id")) or default_client_id(client)
        if client_id in used_ids:
            raise ValueError(f"Duplicate Gemini client ID: {client_id}")
        used_ids.add(client_id)

        add_client_environment(env, env_index, client_id, client)
        env_index += 1

    if env_index == 0:
        print(
            "[WARN] No Gemini account configured; starting in guest mode. "
            "Guest sessions have no conversation history, file uploads, or model choice.",
        )
        add_client_environment(env, 0, GUEST_CLIENT_ID, {})

    return env_index


def build_environment(options: dict[str, Any]) -> dict[str, str]:
    """Overlay the configured options onto the container environment."""
    env = dict(os.environ)

    for option_name, env_name in OPTION_ENV_NAMES.items():
        if option_name not in options:
            continue

        value = format_value(options[option_name])
        if value is None:
            continue

        value = normalize_value(option_name, value)
        env[env_name] = value
        displayed = "***" if option_name in SECRET_FIELDS else value
        print(f"[INFO] {env_name}={displayed}")

    account_count = apply_clients(env, options.get("clients"))
    if account_count == 0:
        # Upstream falls back to the newest cached cookie jar when no
        # __Secure-1PSID is supplied. Give the guest client a path that no
        # previous account could have written to, so removing every account
        # really does start a signed-out session.
        env["GEMINI_COOKIE_PATH"] = f"{GUEST_COOKIE_PATH_PREFIX}-{os.getpid()}"

    return env


def main() -> int:
    """Apply the add-on options and hand the process over to Gemini FastAPI."""
    try:
        options = load_options(OPTIONS_PATH)
    except (OSError, TypeError, UnicodeError, json.JSONDecodeError) as error:
        print(f"[ERROR] Failed to read add-on options: {error}", file=sys.stderr)
        return 1

    try:
        env = build_environment(options)
    except ValueError as error:
        print(f"[ERROR] Invalid add-on option: {error}", file=sys.stderr)
        return 1

    try:
        os.execve(sys.executable, [sys.executable, RUN_SCRIPT], env)
    except (OSError, ValueError) as error:
        print(f"[ERROR] Failed to start Gemini FastAPI: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
