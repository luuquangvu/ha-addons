# Gemini FastAPI Home Assistant add-on

This add-on bundles the upstream [Gemini-FastAPI](https://github.com/Nativu5/Gemini-FastAPI) service so Home Assistant can talk to Google Gemini through an OpenAI-compatible router.

## First-time configuration

After installing the add-on:

1. Start it once so the default configuration files are created in `/homeassistant/gemini-fastapi/config/`.
2. Open `/homeassistant/gemini-fastapi/config/config.yaml` with the Home Assistant file editor (or any editor you prefer).
3. Fill in at least one credential entry with your Gemini cookies:

   ```yaml
   gemini:
     clients:
       - id: "client-a"
         secure_1psid: "YOUR_SECURE_1PSID"
         secure_1psidts: "YOUR_SECURE_1PSIDTS"
   ```

4. Save the file, then restart the add-on from the Add-on panel.

The add-on persists configuration under `/homeassistant/gemini-fastapi/config` and stores conversation data under `/homeassistant/gemini-fastapi/data`, keeping credentials and history across restarts. On updates, a refreshed template is written to `/homeassistant/gemini-fastapi/config/config.yaml.default` so you can compare it with your existing configuration.

### How to obtain Gemini cookies

> [!WARNING]
> Use it with caution and at your own risk, as it's likely against the Google Terms of Service. Consider creating a separate account for this purpose.

1. Open an incognito or private browser window and visit [https://gemini.google.com](https://gemini.google.com), then sign in.
2. Open your browser's developer tools (usually `F12`) and switch to the **Application** tab.
3. Locate the **Storage** > **Cookies** section for `https://gemini.google.com`.
4. Copy the values of `__Secure-1PSID` and `__Secure-1PSIDTS` and paste them into your configuration.
5. Close the incognito or private browser window, then restart the add-on.

### Optional API key

If you want to protect the API with an access token, set it under the `server` section in your configuration:

```yaml
server:
  api_key: "your-strong-secret"
```

### Security notes

- Treat the `secure_1psid` and `secure_1psidts` cookie values like passwords; keep them out of version control and private repositories.
- The add-on exposes port 8000 on the Home Assistant host by default, so set an API key if anyone else shares your network and use HTTPS or a reverse proxy for remote access.

### Home Assistant integration

You can use any OpenAI-compatible integration to connect to this add-on, or try [this integration](https://github.com/luuquangvu/hass_local_openai_llm), which has been specifically modified for it.

## Docker Deployment

### Run with Docker CLI

```bash
docker run -p 8000:8000 \
  -v $(pwd)/gemini-fastapi/data:/app/data \
  -v $(pwd)/gemini-fastapi/cache:/app/cache \
  -e CONFIG_SERVER__API_KEY="your-api-key-here" \
  -e CONFIG_GEMINI__CLIENTS__0__ID="client-a" \
  -e CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID="your-secure-1psid" \
  -e CONFIG_GEMINI__CLIENTS__0__SECURE_1PSIDTS="your-secure-1psidts" \
  -e CONFIG_GEMINI__CLIENTS__0__PROXY="socks5://127.0.0.1:1080" \
  -e GEMINI_COOKIE_PATH="/app/cache" \
  ghcr.io/luuquangvu/gemini-fastapi
```

> [!TIP]
> Add `CONFIG_GEMINI__CLIENTS__N__PROXY` only if you need a proxy; omit the variable to keep direct connections.
>
> `GEMINI_COOKIE_PATH` points to the directory inside the container where refreshed cookies are stored. Bind-mounting it (e.g. `-v $(pwd)/gemini-fastapi/cache:/app/cache`) preserves those cookies across container rebuilds/recreations so you rarely need to re-authenticate.

### Run with Docker Compose

Create a `compose.yaml` file:

```yaml
services:
  gemini-fastapi:
    container_name: gemini-fastapi
    image: ghcr.io/luuquangvu/gemini-fastapi:latest
    volumes:
      # - ./gemini-fastapi/config:/app/config # Uncomment to use a custom config file
      # - ./gemini-fastapi/certs:/app/certs # Uncomment to enable HTTPS with your certs
      - ./gemini-fastapi/data:/app/data
      - ./gemini-fastapi/cache:/app/cache
    restart: on-failure:3 # Avoid retrying too many times
    pull_policy: always
    ports:
      - 8000:8000
    environment:
      - "TZ=Asia/Ho_Chi_Minh" # Set your timezone
      - "CONFIG_SERVER__HOST=0.0.0.0"
      - "CONFIG_SERVER__PORT=8000"
      - "CONFIG_SERVER__API_KEY=your-api-key-here"
      - "CONFIG_GEMINI__CLIENTS__0__ID=client-a"
      - "CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID=your-secure-1psid"
      - "CONFIG_GEMINI__CLIENTS__0__SECURE_1PSIDTS=your-secure-1psidts"
      - "CONFIG_GEMINI__CLIENTS__0__PROXY=socks5://127.0.0.1:1080" # optional per-client proxy
      - "GEMINI_COOKIE_PATH=/app/cache" # must match the cache volume mount above
    healthcheck:
      test:
        [
          "CMD",
          "python",
          "-c",
          "import sys, urllib.request; sys.exit(0) if urllib.request.urlopen('http://localhost:8000/health').getcode() == 200 else sys.exit(1)",
        ]
```

Then run:

```bash
docker compose up -d
```

> [!IMPORTANT]
> Make sure to mount the `/app/data` volume to persist conversation data between container restarts.
> Also mount `/app/cache` so refreshed cookies (including rotated 1PSIDTS values) survive container rebuilds/recreates without re-auth.

## Upstream documentation

Refer to the official project README for advanced settings and authentication details: [https://github.com/Nativu5/Gemini-FastAPI](https://github.com/Nativu5/Gemini-FastAPI).
