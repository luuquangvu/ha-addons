#!/usr/bin/env bash
set -euo pipefail

HOMEASSISTANT_DIR="${HOMEASSISTANT_DIR:-/homeassistant}"
LEGACY_DIR="${LEGACY_DIR:-${HOMEASSISTANT_DIR}/gemini-fastapi}"
LEGACY_CONFIG_DIR="${LEGACY_CONFIG_DIR:-${LEGACY_DIR}/config}"
LEGACY_DATA_DIR="${LEGACY_DATA_DIR:-${LEGACY_DIR}/data}"
MIGRATION_MARKER="${MIGRATION_MARKER:-/data/.homeassistant-migrated}"
DATA_DIR="${DATA_DIR:-/data/storage}"
APP_DIR="${APP_DIR:-/app}"
APP_DATA_DIR="${APP_DATA_DIR:-${APP_DIR}/data}"
PYTHON="${PYTHON:-python}"
RUN_SCRIPT="${RUN_SCRIPT:-${APP_DIR}/apply_options.py}"

echo "[INFO] Starting Gemini FastAPI App..."

mkdir -p "${DATA_DIR}"

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

link_dir() {
  local source="$1"
  local target="$2"

  echo "[INFO] Linking ${target} to ${source}..."

  if [ -L "${target}" ]; then
    if [ "$(readlink "${target}")" = "${source}" ]; then
      echo "[INFO] ${target} is already linked to ${source}."
      return
    fi
    rm -f "${target}"
  fi

  if [ -d "${target}" ] && [ ! -L "${target}" ]; then
    if [ -z "$(ls -A "${source}")" ]; then
      echo "[INFO] Initializing ${source} with default files from ${target}..."
      cp -a "${target}/." "${source}/"
    fi
    rm -rf "${target}"
  elif [ -e "${target}" ]; then
    rm -rf "${target}"
  fi

  ln -s "${source}" "${target}"
}

link_dir "${DATA_DIR}" "${APP_DATA_DIR}"

echo "[INFO] Launching application..."
cd "${APP_DIR}"
exec "${PYTHON}" "${RUN_SCRIPT}"
