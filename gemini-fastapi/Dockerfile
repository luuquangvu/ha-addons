FROM ghcr.io/luuquangvu/gemini-fastapi:20261112-c1fa9b8

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
  io.hass.version="1.0.127"

# Startup preparation runs as root, then hands off to the upstream entrypoint,
# which drops to the unprivileged app user before launching the server.
ENV BASE_ENTRYPOINT=/usr/local/bin/docker-entrypoint.sh

USER root

WORKDIR /app

COPY --chmod=755 scripts/run.sh /app/run.sh
COPY scripts/apply_options.py /app/apply_options.py

ENTRYPOINT ["/usr/bin/tini", "--", "/app/run.sh"]

CMD ["python", "/app/apply_options.py"]
