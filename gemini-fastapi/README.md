# Google Gemini for Home Assistant

[![Home Assistant Add-on](https://img.shields.io/badge/Home%20Assistant-Add--on-blue?style=for-the-badge&logo=home-assistant)](https://github.com/luuquangvu/ha-addons)

**[ 🇺🇸 English | [🇻🇳 Tiếng Việt](README.vi.md) ]**

Integrate Google's state-of-the-art Gemini AI directly into your Home Assistant ecosystem. This Add-on provides an OpenAI-compatible API bridge, empowering Home Assistant Assist, conversation agents, and automation scripts with advanced generative AI capabilities without requiring a Google Cloud API key.

> [!NOTE]
> This Add-on utilizes a specialized fork of [Gemini-FastAPI](https://github.com/luuquangvu/Gemini-FastAPI) optimized for seamless Home Assistant integration and rapid updates.

---

## Technical Features

- **OpenAI-Compatible API**: Seamlessly integrates with any Home Assistant component or third-party client supporting the OpenAI API standard.
- **Model Support**: Access Gemini Pro, Gemini Flash Thinking, and Gemini Flash models.
- **Cookie-Based Authentication**: Access Gemini via standard browser session cookies, bypassing complex Google Cloud Project configurations.
- **Conversation Context**: Supports multi-turn dialogue with memory, enabling more natural interactions for smart home control.
- **Google Search Grounding**: Leverages real-time web information for accurate response generation.
- **Multimodal Capabilities**: Native support for processing text, images, and file attachments in automations.
- **Home Assistant Optimized**: Designed for local execution with simple configuration via YAML or environment variables.

---

## Security and Privacy Considerations

- **Authentication Method**: This Add-on uses browser cookies to authenticate with Google Gemini services. Be aware that this may violate Google's Terms of Service, which could result in account restrictions.
- **Recommended Practice**: It is strongly advised to use a **dedicated secondary Google account** for this integration to safeguard your primary account data.

---

## Installation and Configuration

### Step 1: Add-on Installation

1. Add the [**luuquangvu/ha-addons**](https://github.com/luuquangvu/ha-addons) repository to your Home Assistant Add-on Store.
2. Locate and install **Gemini FastAPI**.
3. **Start the Add-on once.** The service will initialize default configuration files and then stop automatically.

### Step 2: Extract Authentication Cookies

1. Open a **Private/Incognito** browser window.
2. Log in to [https://gemini.google.com](https://gemini.google.com) with your secondary Google account.
3. Open **Developer Tools** (F12 or Right-click > Inspect).
4. Navigate to the **Application** tab (Chrome/Edge) or **Storage** tab (Firefox).
5. Under **Cookies**, select `https://gemini.google.com` and locate the following values:
   - `__Secure-1PSID`
   - `__Secure-1PSIDTS`
6. **Close the incognito window immediately** after copying to prevent session conflicts.

### Step 3: Service Configuration

1. Use a file editor (e.g., Studio Code Server) to access `/homeassistant/gemini-fastapi/config/`.
2. Edit `config.yaml` to include your extracted cookies:

   ```yaml
   gemini:
     clients:
       - id: "ha-gemini"
         secure_1psid: "PASTE_YOUR_SECURE_1PSID_HERE"
         secure_1psidts: "PASTE_YOUR_SECURE_1PSIDTS_HERE"
   ```

3. **(Recommended)** Secure your API endpoint by defining a secret token:

   ```yaml
   server:
     api_key: "your-super-secret-token"
   ```

### Step 4: Deployment

1. Return to the Gemini FastAPI Add-on page and click **Start**.
2. Review the **Log** tab to verify successful service initialization.

---

## Home Assistant Integration

To utilize Gemini as a conversation agent, we recommend the [**Local OpenAI LLM**](https://github.com/luuquangvu/hass_local_openai_llm) integration.

1. **Install via HACS**:
   [![Open HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=luuquangvu&repository=hass_local_openai_llm&category=integration)
2. **Add the Integration**: Navigate to **Settings > Devices & Services** and search for "Local OpenAI LLM".
3. **Connection Settings**:
   - **Base URL**: `http://YOUR_HA_IP:8000/v1` (or `http://127.0.0.1:8000/v1` if running on the same host)
   - **API Key**: The `api_key` defined in your `config.yaml`.

---

## Containerized Deployment (Docker)

### Docker Compose

```yaml
services:
  gemini-fastapi:
    image: ghcr.io/luuquangvu/gemini-fastapi:latest
    container_name: gemini-fastapi
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./cache:/app/cache
    environment:
      - "TZ=Asia/Ho_Chi_Minh"
      - "CONFIG_SERVER__API_KEY=your-api-key"
      - "CONFIG_GEMINI__CLIENTS__0__ID=main-client"
      - "CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID=your-1psid"
      - "CONFIG_GEMINI__CLIENTS__0__SECURE_1PSIDTS=your-1psidts"
      - "GEMINI_COOKIE_PATH=/app/cache"
```

### Docker CLI

```bash
docker run -d --name gemini-fastapi \
  -p 8000:8000 \
  -v ./data:/app/data \
  -v ./cache:/app/cache \
  -e "CONFIG_SERVER__API_KEY=your-api-key" \
  -e "CONFIG_GEMINI__CLIENTS__0__ID=main-client" \
  -e "CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID=your-1psid" \
  -e "CONFIG_GEMINI__CLIENTS__0__SECURE_1PSIDTS=your-1psidts" \
  -e "GEMINI_COOKIE_PATH=/app/cache" \
  ghcr.io/luuquangvu/gemini-fastapi:latest
```

---

## Troubleshooting

- **Authentication Failure**: If the log indicates initialization failure, your session cookies may have expired. Please repeat the extraction process.
- **Connection Issues**: Verify that port `8000` is accessible and the `api_key` matches your Home Assistant configuration.
- **Session Stability**: If cookies expire frequently, consider using a different browser engine for extraction (e.g., Firefox).

---

## Credits

- Built upon the [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API) library.
