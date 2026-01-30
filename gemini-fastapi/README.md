# Gemini FastAPI - Home Assistant Add-on

[![GitHub License](https://img.shields.io/github/license/luuquangvu/ha-addons?style=for-the-badge&labelColor=000000)](https://github.com/luuquangvu/ha-addons/blob/main/LICENSE)

This add-on integrates the Gemini-FastAPI service with Home Assistant. It exposes an OpenAI-compatible API that allows Home Assistant, and other clients, to interact with Google's Gemini models without needing an official API key, allowing completely free and unlimited use.

> This add-on uses a fork of the upstream project ([luuquangvu/Gemini-FastAPI](https://github.com/luuquangvu/Gemini-FastAPI)) to roll out updates faster.

## Features

- **Completely Free And Unlimited Use**: Access the latest Gemini models at no cost, just like you do with your browser.
- **No Google API Key Required**: Access Gemini models using only browser cookies.
- **Conversation Persistence**: Retain conversation history across restarts.
- **Google Search Integration**: Provides up-to-date, web-grounded answers.
- **Multi-modal Support**: Handle text, image, and file inputs.
- **Flexible Configuration**: Configure via YAML files or environment variables.

---

## Important: Before You Begin

- **Risk of Use**: Using your browser cookies to access Gemini may violate Google's Terms of Service. This could potentially lead to restrictions on your Google account.
- **Recommendation**: To minimize risk, it is strongly recommended that you **use a secondary, non-primary Google account** for this add-on.

---

## Add-on Installation & Configuration

### Step 1: Install the Add-on

1. Ensure you have added the [**Home Assistant Add-ons Repository**](https://github.com/luuquangvu/ha-addons) to your Add-on Store.
2. Find and install the **Gemini FastAPI** add-on.
3. **Start the add-on once.** This will generate the necessary configuration files and then stop.

### Step 2: Get Your Google Gemini Cookies

1. Open a **Private or Incognito** browser window.
2. Go to [https://gemini.google.com](https://gemini.google.com) and sign in with your chosen Google account (a secondary account is recommended).
3. Open the browser's Developer Tools (usually by pressing `F12`).
4. Go to the **Application** > **Storage** tab.
5. Under the **Cookies** section for `https://gemini.google.com`, find and copy the values for:
   - `__Secure-1PSID`
   - `__Secure-1PSIDTS`
6. Keep these values ready.
7. **Close the incognito window immediately** after copying the values and proceed to the next step promptly. This helps prevent cookie synchronization issues or premature expiration.

### Step 3: Configure the Add-on

1. Using a file editor (like the Studio Code Server add-on or via Samba), navigate to the `/homeassistant/gemini-fastapi/config/` directory created in Step 1.
2. Open the `config.yaml` file.
3. Fill in your cookie values from Step 2:

   ```yaml
   gemini:
     clients:
       - id: "client-a" # or any other name
         secure_1psid: "PASTE_YOUR_SECURE_1PSID_VALUE_HERE"
         secure_1psidts: "PASTE_YOUR_SECURE_1PSIDTS_VALUE_HERE"
   ```

4. (Optional, but Recommended) To protect the API endpoint with a token, add an `api_key` under the `server` section:

   ```yaml
   server:
     api_key: "your-strong-secret-token"
   ```

5. Save the `config.yaml` file.

### Step 4: Restart and Verify

1. Return to the Gemini FastAPI add-on page in Home Assistant.
2. Click **Restart**.
3. Check the **Log** tab to ensure the add-on starts successfully.

> [!NOTE]
> The add-on exposes port 8000 on your Home Assistant host. It is strongly recommended to set an API key (as shown in Step 3) to protect this endpoint, especially if your network is not private. For remote access, always use a secure reverse proxy like Nginx Proxy Manager.

### Troubleshooting & Cookie Updates

Since this add-on relies on browser cookies, they may expire over time (e.g., if you log out of Google or the session times out).

- **Symptoms**: The add-on stops responding, or you see `Failed to initialize client ...` errors in the Logs.
- **Fix**: Simply repeat **Step 2** and **Step 3** to fetch new cookies and update your `config.yaml`, then restart the add-on.

> [!NOTE]
> If you frequently encounter cookie expiration issues, try retrieving the cookies from a different browser.

### Connecting to Home Assistant

To use Gemini within Home Assistant's Assist pipelines, you need an integration that supports OpenAI-compatible APIs.

#### Recommended: Local OpenAI LLM

We strongly recommend using the [**Local OpenAI LLM**](https://github.com/luuquangvu/hass_local_openai_llm) custom integration. This is a fork specifically optimized for this add-on, supporting local LLM servers out of the box.

1.  **Install via HACS**:
    - **Automatic**: Click the button below to open the repository directly in HACS:

      [![Open HACS Repository](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=luuquangvu&repository=hass_local_openai_llm&category=integration)

    - **Manual**: If the button doesn't work, add `https://github.com/luuquangvu/hass_local_openai_llm` as a **Custom Repository** (Category: Integration) in HACS.

    - Click **Download** and **Restart** Home Assistant once the download is complete.

2.  **Add Integration**: Navigate to **Settings > Devices & Services**, click **Add Integration**, and search for **Local OpenAI LLM**.

3.  **Configure**:
    - **Server URL**: `http://127.0.0.1:8000/v1`
    - **API Key**: The key you defined in your `config.yaml` (leave blank if not set).

---

## Standalone Docker Deployment

For users running the service outside Home Assistant.

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
      # - "CONFIG_GEMINI__CLIENTS__0__PROXY=socks5://127.0.0.1:1080" # Uncomment to enable proxy for each client
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
# -e "CONFIG_GEMINI__CLIENTS__0__PROXY=socks5://127.0.0.1:1080" \
  -e "GEMINI_COOKIE_PATH=/app/cache" \
  --restart on-failure:3 \
  ghcr.io/luuquangvu/gemini-fastapi:latest
```

> [!IMPORTANT]
>
> - Mount `/app/data` to persist conversation history.
> - Mount `/app/cache` to preserve refreshed cookies and avoid frequent re-authentication.

---

## Custom Models

You can define custom models in `config.yaml` or via environment variables.

### YAML Configuration

```yaml
gemini:
  model_strategy: "append" # "append" (default + custom) or "overwrite" (custom only)
  models:
    - model_name: "gemini-3.0-pro"
      model_header:
        x-goog-ext-525001261-jspb: '[1,null,null,null,"9d8ca3786ebdfbea",null,null,0,[4],null,null,1]'
```

### Environment Variables

You can supply models as a JSON string or list structure via `CONFIG_GEMINI__MODELS`. This provides a flexible way to override settings via the shell or in automated environments (e.g. Docker) without modifying the configuration file.

```bash
export CONFIG_GEMINI__MODEL_STRATEGY="overwrite"
export CONFIG_GEMINI__MODELS='[{"model_name": "gemini-3.0-pro", "model_header": {"x-goog-ext-525001261-jspb": "[1,null,null,null,\"9d8ca3786ebdfbea\",null,null,0,[4],null,null,1]"}}]'
```

---

## Acknowledgments

- **Upstream Service**: [Nativu5/Gemini-FastAPI](https://github.com/Nativu5/Gemini-FastAPI)
- **Gemini API Client**: [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API)
