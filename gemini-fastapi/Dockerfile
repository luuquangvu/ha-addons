FROM ghcr.io/luuquangvu/gemini-fastapi:20260826-c17e912

LABEL \
  org.opencontainers.image.title="Gemini FastAPI" \
  org.opencontainers.image.description="OpenAI-compatible router that proxies Google Gemini for Home Assistant." \
  org.opencontainers.image.url="https://github.com/luuquangvu/ha-addons/tree/main/gemini-fastapi" \
  org.opencontainers.image.documentation="https://github.com/luuquangvu/ha-addons/blob/main/gemini-fastapi/README.md" \
  org.opencontainers.image.authors="Luu Quang Vu <https://github.com/luuquangvu>" \
  org.opencontainers.image.vendor="Luu Quang Vu" \
  org.opencontainers.image.licenses="MIT" \
  io.hass.name="Gemini FastAPI" \
  io.hass.description="OpenAI-compatible router that proxies Google Gemini for Home Assistant." \
  io.hass.arch="amd64|aarch64" \
  io.hass.type="addon" \
  io.hass.version="1.0.115"

# tally ignore=hadolint/DL3002
USER root

WORKDIR /app

RUN <<EOF
set -eux
/app/.venv/bin/python -m ensurepip --upgrade
/app/.venv/bin/python -m pip install --no-cache-dir ruamel.yaml
EOF

COPY --chmod=755 scripts/run.sh /app/run.sh
COPY scripts/merge_config.py /app/merge_config.py

CMD ["/app/run.sh"]
