FROM ghcr.io/luuquangvu/gemini-fastapi:latest

WORKDIR /app

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --chmod=755 run.sh /app/run.sh

ENTRYPOINT ["./run.sh"]

HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1
