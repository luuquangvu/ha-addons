FROM ghcr.io/luuquangvu/gemini-fastapi:20260425-b8cd546

LABEL \
  io.hass.name="Gemini FastAPI" \
  io.hass.description="OpenAI-compatible router that proxies Google Gemini for Home Assistant." \
  io.hass.arch="amd64|aarch64" \
  io.hass.type="addon" \
  io.hass.version="1.0.89" \
  org.opencontainers.image.title="Gemini FastAPI" \
  org.opencontainers.image.description="OpenAI-compatible router that proxies Google Gemini for Home Assistant." \
  org.opencontainers.image.vendor="Luu Quang Vu" \
  org.opencontainers.image.authors="Luu Quang Vu <https://github.com/luuquangvu>" \
  org.opencontainers.image.licenses="MIT" \
  org.opencontainers.image.url="https://github.com/luuquangvu/ha-addons/tree/main/gemini-fastapi" \
  org.opencontainers.image.source="https://github.com/luuquangvu/ha-addons" \
  org.opencontainers.image.documentation="https://github.com/luuquangvu/ha-addons/blob/main/gemini-fastapi/README.md"

USER root

WORKDIR /app

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

COPY --chmod=755 run.sh /app/run.sh

CMD ["/app/run.sh"]
