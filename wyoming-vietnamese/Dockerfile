FROM ghcr.io/luuquangvu/wyoming-vietnamese:20260811-3e801eb

LABEL \
  io.hass.name="Wyoming Vietnamese" \
  io.hass.description="Vietnamese speech-to-text and text-to-speech over the Wyoming protocol." \
  io.hass.arch="amd64|aarch64" \
  io.hass.type="addon" \
  io.hass.version="1.0.0" \
  org.opencontainers.image.title="Wyoming Vietnamese" \
  org.opencontainers.image.description="Vietnamese speech-to-text and text-to-speech over the Wyoming protocol." \
  org.opencontainers.image.vendor="Luu Quang Vu" \
  org.opencontainers.image.authors="Luu Quang Vu <https://github.com/luuquangvu>" \
  org.opencontainers.image.licenses="MIT" \
  org.opencontainers.image.url="https://github.com/luuquangvu/ha-addons/tree/main/wyoming-vietnamese" \
  org.opencontainers.image.source="https://github.com/luuquangvu/ha-addons" \
  org.opencontainers.image.documentation="https://github.com/luuquangvu/ha-addons/blob/main/wyoming-vietnamese/README.md"

USER root

WORKDIR /app

COPY --chmod=755 scripts/run.sh /app/run.sh
COPY scripts/apply_options.py /app/apply_options.py

CMD ["/app/run.sh"]
