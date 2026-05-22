#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/homeassistant/gemini-fastapi"
CONFIG_DIR="${BASE_DIR}/config"
DATA_DIR="${BASE_DIR}/data"
CACHE_DIR="/data/cache"
APP_CONFIG_DIR="/app/config"
APP_DATA_DIR="/app/data"
CONFIG_FILE="config.yaml"
ORIGINAL_CONFIG_FILE="config.yaml.default"
CONFIG_BACKUP_FILE="config.yaml.bak"

echo "[INFO] Starting Gemini FastAPI App..."

mkdir -p "${CONFIG_DIR}" "${DATA_DIR}" "${CACHE_DIR}"
chown -R "$(id -u):$(id -g)" "${CONFIG_DIR}" "${DATA_DIR}" "${CACHE_DIR}" || true
chmod -R 755 "${CONFIG_DIR}" "${DATA_DIR}" "${CACHE_DIR}" || true

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

if [ -d "${APP_CONFIG_DIR}" ] && [ ! -L "${APP_CONFIG_DIR}" ] && [ -z "$(ls -A "${CONFIG_DIR}")" ]; then
  echo "[INFO] Initializing ${CONFIG_DIR} with default files from ${APP_CONFIG_DIR}..."
  cp -a "${APP_CONFIG_DIR}/." "${CONFIG_DIR}/"
fi

if [ -f "${APP_CONFIG_DIR}/${CONFIG_FILE}" ] && [ ! -L "${APP_CONFIG_DIR}" ]; then
  echo "[INFO] Merging config defaults into user config..."
  uv run --no-dev --with ruamel.yaml /app/merge_config.py \
    --default "${APP_CONFIG_DIR}/${CONFIG_FILE}" \
    --user "${CONFIG_DIR}/${CONFIG_FILE}" \
    --state "${CONFIG_DIR}/${ORIGINAL_CONFIG_FILE}" \
    --backup "${CONFIG_DIR}/${CONFIG_BACKUP_FILE}"
else
  echo "[WARN] Default config ${APP_CONFIG_DIR}/${CONFIG_FILE} not found; skipping config merge."
fi

link_dir "${CONFIG_DIR}" "${APP_CONFIG_DIR}"
link_dir "${DATA_DIR}" "${APP_DATA_DIR}"

echo "[INFO] Launching application..."
cd /app
exec uv run --no-dev run.py
