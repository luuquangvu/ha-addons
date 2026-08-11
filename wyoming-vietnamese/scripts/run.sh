#!/usr/bin/env bash
set -euo pipefail

CACHE_DIR="${CACHE_DIR:-/data/cache}"
DOWNLOAD_DIR="${DOWNLOAD_DIR:-/data/models}"

echo "[INFO] Starting Wyoming Vietnamese App..."

mkdir -p "${CACHE_DIR}" "${DOWNLOAD_DIR}"
chmod 755 "${CACHE_DIR}" "${DOWNLOAD_DIR}" || true

echo "[INFO] Model storage: cache=${CACHE_DIR}, models=${DOWNLOAD_DIR}"
echo "[INFO] Launching application..."

cd /app
exec python /app/apply_options.py
