#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="/config/gemini-fastapi"
STATE_BASE="/data/gemini-fastapi"
DATA_DIR="${STATE_BASE}/data"
CACHE_DIR="${STATE_BASE}/cache"

mkdir -p "${CONFIG_DIR}" "${DATA_DIR}" "${CACHE_DIR}"

# Replace the application directories with symlinks into Home Assistant storage.
link_dir() {
    local source="$1"
    local target="$2"
    local backup="${3:-}"

    if [ -d "${target}" ] && [ ! -L "${target}" ]; then
        if [ -z "$(ls -A "${source}")" ]; then
            cp -a "${target}/." "${source}/"
        elif [ -n "${backup}" ]; then
            mkdir -p "$(dirname "${backup}")"
            rm -rf "${backup}"
            if [[ "${backup}" == *.yaml ]] && [ -f "${target}/config.yaml" ]; then
                cp -a "${target}/config.yaml" "${backup}"
            else
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

link_dir "${CONFIG_DIR}" "/app/config" "${CONFIG_DIR}/config.yaml.default"
link_dir "${DATA_DIR}" "/app/data"
link_dir "${CACHE_DIR}" "/app/cache"

cd /app
exec uv run --no-dev run.py
