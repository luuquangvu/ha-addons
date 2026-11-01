#!/usr/bin/env bash
set -euo pipefail

CACHE_DIR="${CACHE_DIR:-/data/cache}"
DOWNLOAD_DIR="${DOWNLOAD_DIR:-/data/models}"
APP_UID="${APP_UID:-1000}"
APP_GID="${APP_GID:-1000}"
PRIVILEGE_MARKER="${PRIVILEGE_MARKER:-/data/.app-uid-${APP_UID}-${APP_GID}}"
export APP_UID APP_GID

echo "[INFO] Starting Wyoming Vietnamese App..."

mkdir -p "${CACHE_DIR}" "${DOWNLOAD_DIR}"

# Fix ownership once after an upgrade, or when the target directories were
# recreated with the wrong owner. Re-running chown -R on every start is slow
# with multi-gigabyte model directories.
if
  [ ! -f "${PRIVILEGE_MARKER}" ] \
    || [ "$(stat -c '%u:%g' "${CACHE_DIR}")" != "${APP_UID}:${APP_GID}" ] \
    || [ "$(stat -c '%u:%g' "${DOWNLOAD_DIR}")" != "${APP_UID}:${APP_GID}" ]
then
  if chown -R "${APP_UID}:${APP_GID}" "${CACHE_DIR}" "${DOWNLOAD_DIR}"; then
    : > "${PRIVILEGE_MARKER}"
  else
    echo "[WARN] Could not update ownership of ${CACHE_DIR} and ${DOWNLOAD_DIR}; retrying on the next start." >&2
  fi
fi

chmod 755 "${CACHE_DIR}" "${DOWNLOAD_DIR}" || true

echo "[INFO] Model storage: cache=${CACHE_DIR}, models=${DOWNLOAD_DIR}"
echo "[INFO] Launching application..."

cd /app
exec python /app/apply_options.py
