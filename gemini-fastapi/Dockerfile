FROM ghcr.io/nativu5/gemini-fastapi:latest

WORKDIR /app

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash \
    && rm -rf /var/lib/apt/lists/*

COPY --chmod=755 run.sh /app/run.sh

ENTRYPOINT ["./run.sh"]
