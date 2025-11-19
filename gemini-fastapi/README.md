# Gemini FastAPI - Home Assistant Add-on

[![GitHub License](https://img.shields.io/github/license/luuquangvu/ha-addons?style=for-the-badge&labelColor=000000)](https://github.com/luuquangvu/ha-addons/blob/main/LICENSE)

This add-on integrates the [Gemini-FastAPI](https://github.com/Nativu5/Gemini-FastAPI) service with Home Assistant. It exposes an OpenAI-compatible API that allows Home Assistant, and other clients, to interact with Google's Gemini models without needing an official API key.

> This add-on uses a fork of the upstream project ([luuquangvu/Gemini-FastAPI](https://github.com/luuquangvu/Gemini-FastAPI)) to roll out updates faster.

## Features

- **No Google API Key Required**: Accesses Gemini models using only browser cookies.
- **Conversation Persistence**: Retains conversation history across restarts.
- **Google Search Integration**: Provides up-to-date, web-grounded answers.
- **Multi-modal Support**: Handles text, image, and file inputs.
- **Flexible Configuration**: Configure via YAML files or environment variables.

---

## Important: Before You Begin

- **Risk of Use**: Using your browser cookies to access Gemini may violate Google's Terms of Service. This could potentially lead to restrictions on your Google account.
- **Recommendation**: To minimize risk, it is strongly recommended that you **use a secondary, non-primary Google account** for this add-on.

---

## Add-on Installation & Configuration

### Step 1: Get Your Google Gemini Cookies

Before installing, obtain the necessary cookies for authentication.

1. Open a **Private or Incognito** browser window.
2. Go to [https://gemini.google.com](https://gemini.google.com) and sign in with your chosen Google account (a secondary account is recommended).
3. Open the browser's Developer Tools (usually by pressing `F12`).
4. Go to the **Application** > **Storage** tab.
5. Under the **Cookies** section for `https://gemini.google.com`, find and copy the values for:
   - `__Secure-1PSID`
   - `__Secure-1PSIDTS`
6. Keep these values ready.

### Step 2: Install and Configure the Add-on

1. In Home Assistant, navigate to **Settings > Add-ons > Add-on Store**.
2. Click the 3-dots menu, select **Repositories**, and add this URL:

   ```text
   https://github.com/luuquangvu/ha-addons
   ```

3. Install the **Gemini FastAPI** add-on.
4. **Start the add-on once.** This will generate the necessary configuration files and then stop.
5. Using a file editor (like the Studio Code Server add-on or via Samba), navigate to the `/homeassistant/gemini-fastapi/config/` directory.
6. Open the `config.yaml` file.
7. Fill in your cookie values that you obtained in Step 1:

   ```yaml
   gemini:
     clients:
       - id: "client-a" # or any other name
         secure_1psid: "PASTE_YOUR_SECURE_1PSID_VALUE_HERE"
         secure_1psidts: "PASTE_YOUR_SECURE_1PSIDTS_VALUE_HERE"
   ```

8. (Optional, but Recommended) To protect the API endpoint with a token, add an `api_key` under the `server` section:

   ```yaml
   server:
     api_key: "your-strong-secret-token"
   ```

9. Save the `config.yaml` file.

### Step 3: Restart and Verify

1. Return to the Gemini FastAPI add-on page in Home Assistant.
2. Click **Restart**.
3. Check the **Log** tab to ensure the add-on starts successfully without any cookie-related errors.

> [!NOTE]
> The add-on exposes port 8000 on your Home Assistant host. It is strongly recommended to set an API key (as shown in Step 2) to protect this endpoint, especially if your network is not private. For remote access, always use a secure reverse proxy like Nginx Proxy Manager.

### Connecting to Home Assistant

You can connect this add-on to Home Assistant using any OpenAI-compatible integration. For the best experience, try the [**Local OpenAI LLM**](https://github.com/luuquangvu/hass_local_openai_llm) custom integration, which is optimized for this add-on.

---

## Standalone Docker Deployment

For users running the service outside of Home Assistant.

### Using Docker Compose

Create a `compose.yaml`:

```yaml
services:
  gemini-fastapi:
    container_name: gemini-fastapi
    image: ghcr.io/luuquangvu/gemini-fastapi:latest
    pull_policy: always
    restart: on-failure:3
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./cache:/app/cache
      # - ./config:/app/config # Uncomment to use a config file instead of env vars
      # - ./certs:/app/certs # Uncomment to enable HTTPS
    environment:
      - "TZ=Asia/Ho_Chi_Minh" # Set your timezone
      - "CONFIG_SERVER__HOST=0.0.0.0"
      - "CONFIG_SERVER__PORT=8000"
      - "CONFIG_SERVER__API_KEY=your-api-key-here"
      - "CONFIG_GEMINI__CLIENTS__0__ID=client-a"
      - "CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID=your-secure-1psid"
      - "CONFIG_GEMINI__CLIENTS__0__SECURE_1PSIDTS=your-secure-1psidts"
      - "CONFIG_GEMINI__CLIENTS__0__PROXY=socks5://127.0.0.1:1080" # Optional
      - "GEMINI_COOKIE_PATH=/app/cache"
    healthcheck:
      test:
        [
          "CMD",
          "python",
          "-c",
          "import sys, urllib.request; sys.exit(0) if urllib.request.urlopen('http://localhost:8000/health').getcode() == 200 else sys.exit(1)",
        ]
```

Then launch it: `docker compose up -d`

### Using Docker CLI

```bash
docker run -d --name gemini-fastapi \
  -p 8000:8000 \
  -v ./data:/app/data \
  -v ./cache:/app/cache \
  -e "CONFIG_SERVER__API_KEY=your-api-key-here" \
  -e "CONFIG_GEMINI__CLIENTS__0__ID=client-a" \
  -e "CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID=your-secure-1psid" \
  -e "CONFIG_GEMINI__CLIENTS__0__SECURE_1PSIDTS=your-secure-1psidts" \
  -e "CONFIG_GEMINI__CLIENTS__0__PROXY=socks5://127.0.0.1:1080" # Optional
  -e "GEMINI_COOKIE_PATH=/app/cache" \
  --restart on-failure:3 \
  ghcr.io/luuquangvu/gemini-fastapi:latest
```

> [!IMPORTANT]
>
> - Mount `/app/data` to persist conversation history.
> - Mount `/app/cache` to preserve refreshed cookies and avoid frequent re-authentication.

---

## Acknowledgments

- **Upstream Service**: [Nativu5/Gemini-FastAPI](https://github.com/Nativu5/Gemini-FastAPI)
- **Gemini API Client**: [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API)
