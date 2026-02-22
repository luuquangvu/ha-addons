#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/homeassistant/gemini-fastapi"
CONFIG_DIR="${BASE_DIR}/config"
DATA_DIR="${BASE_DIR}/data"
CACHE_DIR="/data/cache"
CONFIG_FILE="config.yaml"
ORIGINAL_CONFIG_FILE="config.yaml.default"

echo "[INFO] Starting Gemini FastAPI Add-on..."

mkdir -p "${CONFIG_DIR}" "${DATA_DIR}" "${CACHE_DIR}"
chown -R "$(id -u):$(id -g)" "${CONFIG_DIR}" "${DATA_DIR}" "${CACHE_DIR}" || true
chmod -R 755 "${CONFIG_DIR}" "${DATA_DIR}" "${CACHE_DIR}" || true

link_dir() {
    local source="$1"
    local target="$2"
    local backup="${3:-}"

    echo "[INFO] Linking ${target} to ${source}..."

    if [ -d "${target}" ] && [ ! -L "${target}" ]; then
        if [ -z "$(ls -A "${source}")" ]; then
            echo "[INFO] Initializing ${source} with default files from ${target}..."
            cp -a "${target}/." "${source}/"
        elif [ -n "${backup}" ]; then
            mkdir -p "$(dirname "${backup}")"
            rm -f "${backup}"
            
            if [[ "${backup}" == */${ORIGINAL_CONFIG_FILE} ]] && [ -f "${target}/${CONFIG_FILE}" ]; then
                cp -a "${target}/${CONFIG_FILE}" "${backup}"
            else
                rm -rf "${backup}"
                mkdir -p "${backup}"
                cp -a "${target}/." "${backup}/"
            fi
        fi
        rm -rf "${target}"
    elif [ -e "${target}" ]; then
        rm -rf "${target}"
    fi

    ln -s "${source}" "${target}"
}

link_dir "${CONFIG_DIR}" "/app/config" "${CONFIG_DIR}/${ORIGINAL_CONFIG_FILE}"
link_dir "${DATA_DIR}" "/app/data"

echo "[INFO] Launching application..."
cd /app
exec uv run --no-dev run.py
