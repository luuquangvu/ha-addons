#!/bin/sh
set -eu

HOMEASSISTANT_DIR="${HOMEASSISTANT_DIR:-/homeassistant}"
LEGACY_DIR="${LEGACY_DIR:-${HOMEASSISTANT_DIR}/gemini-fastapi}"
LEGACY_CONFIG_DIR="${LEGACY_CONFIG_DIR:-${LEGACY_DIR}/config}"
LEGACY_DATA_DIR="${LEGACY_DATA_DIR:-${LEGACY_DIR}/data}"
MIGRATION_MARKER="${MIGRATION_MARKER:-/data/.homeassistant-migrated}"
DATA_ROOT="${DATA_ROOT:-/data}"
DATA_DIR="${DATA_DIR:-${DATA_ROOT}/storage}"
CACHE_DIR="${CACHE_DIR:-${GEMINI_COOKIE_PATH:-${DATA_ROOT}/cache}}"
OPTIONS_FILE="${OPTIONS_FILE:-${DATA_ROOT}/options.json}"
APP_UID="${APP_UID:-$(id -u app)}"
APP_GID="${APP_GID:-$(id -g app)}"
APP_DIR="${APP_DIR:-/app}"
PYTHON="${PYTHON:-python}"
RUN_SCRIPT="${RUN_SCRIPT:-${APP_DIR}/apply_options.py}"
BASE_ENTRYPOINT="${BASE_ENTRYPOINT:-}"

echo "[INFO] Starting Gemini FastAPI App..."

mkdir -p "${DATA_ROOT}" "${DATA_DIR}" "${CACHE_DIR}"

# The Supervisor creates /data and options.json as root; options.json is mode
# 0600. Hand them to the runtime user before the base entrypoint drops root.
if [ "$(id -u)" -eq 0 ]; then
  chown "${APP_UID}:${APP_GID}" "${DATA_ROOT}"
  if [ -e "${OPTIONS_FILE}" ]; then
    chown "${APP_UID}:${APP_GID}" "${OPTIONS_FILE}"
  fi
fi

# The homeassistant_config mount is used only to retire the old layout.
# Conversation data is copied before the old config is removed, and an existing
# /data/storage is never overwritten, so a failed or repeated migration cannot
# discard the current conversation store.
if [ ! -f "${MIGRATION_MARKER}" ]; then
  if [ -d "${HOMEASSISTANT_DIR}" ]; then
    migration_complete=1

    if [ -d "${LEGACY_DATA_DIR}" ]; then
      if [ -z "$(ls -A "${DATA_DIR}")" ]; then
        echo "[INFO] Moving conversation data from ${LEGACY_DATA_DIR} to ${DATA_DIR}..."
        cp -a "${LEGACY_DATA_DIR}/." "${DATA_DIR}/"
        rm -rf -- "${LEGACY_DATA_DIR}"
      else
        echo "[WARN] ${DATA_DIR} already contains data; not overwriting it with ${LEGACY_DATA_DIR}. Remove or move the legacy data folder to finish the migration." >&2
        migration_complete=0
      fi
    fi

    if [ "${migration_complete}" -eq 1 ]; then
      if [ -e "${LEGACY_CONFIG_DIR}" ] || [ -L "${LEGACY_CONFIG_DIR}" ]; then
        echo "[INFO] Removing legacy configuration directory ${LEGACY_CONFIG_DIR}; settings now live in the Configuration tab."
        rm -rf -- "${LEGACY_CONFIG_DIR}"
      fi
      : > "${MIGRATION_MARKER}"
    fi
  else
    echo "[WARN] ${HOMEASSISTANT_DIR} is not available; the one-time migration runs on a later start." >&2
  fi
fi

# Hand the persistent directories to the runtime user. The ownership check
# avoids a recursive chown on every restart once the change is in place.
if [ "$(id -u)" -eq 0 ]; then
  for dir in "${DATA_DIR}" "${CACHE_DIR}"; do
    if [ "$(stat -c '%u:%g' "${dir}")" != "${APP_UID}:${APP_GID}" ]; then
      chown -R "${APP_UID}:${APP_GID}" "${dir}"
    fi
  done
fi

echo "[INFO] Launching application..."
if [ -n "${BASE_ENTRYPOINT}" ]; then
  if [ ! -x "${BASE_ENTRYPOINT}" ]; then
    echo "[ERROR] Required base entrypoint not found: ${BASE_ENTRYPOINT}" >&2
    exit 1
  fi
  exec "${BASE_ENTRYPOINT}" "$@"
fi
cd "${APP_DIR}"
exec "${PYTHON}" "${RUN_SCRIPT}"
