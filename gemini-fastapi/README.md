# Google Gemini for Home Assistant

[![Home Assistant App](https://img.shields.io/badge/Home%20Assistant-Add--on-blue?style=for-the-badge&logo=home-assistant)](https://github.com/luuquangvu/ha-addons)

**🇺🇸 English | [🇻🇳 Tiếng Việt](README.vi.md)**

Integrate Google's state-of-the-art Gemini AI directly into your Home Assistant ecosystem. This App provides an OpenAI-compatible API bridge, empowering Home Assistant Assist, conversation agents, and automation scripts with advanced generative AI capabilities without requiring a Google Cloud API key.

> [!NOTE]
> This App utilizes a specialized fork of [Gemini-FastAPI](https://github.com/luuquangvu/Gemini-FastAPI) optimized for seamless Home Assistant integration and rapid updates.

---

## Technical Features

- **OpenAI-Compatible API**: Seamlessly integrates with any Home Assistant component or third-party client supporting the OpenAI API standard.
- **Model Support**: Access Gemini Pro, Gemini Flash Thinking, and Gemini Flash models.
- **Cookie-Based Authentication**: Access Gemini via standard browser session cookies, bypassing complex Google Cloud Project configurations.
- **Conversation Context**: Supports multi-turn dialogue with memory, enabling more natural interactions for smart home control.
- **Google Search Grounding**: Leverages real-time web information for accurate response generation.
- **Multimodal Capabilities**: Native support for processing text, images, and file attachments in automations.
- **Multi-Account Support**: Add multiple Gemini accounts to spread requests across them and reduce rate limits.
- **Home Assistant Optimized**: Designed for local execution with simple configuration from the App's **Configuration** tab.

---

## Security and Privacy Considerations

- **Authentication Method**: This App uses browser cookies to authenticate with Google Gemini services. Be aware that this may violate Google's Terms of Service, which could result in account restrictions.
- **Recommended Practice**: It is strongly advised to use a **dedicated secondary Google account** for this integration to safeguard your primary account data.

---

## Installation and Configuration

### Step 1: App Installation

1. Add the [**luuquangvu/ha-addons**](https://github.com/luuquangvu/ha-addons) repository to your Home Assistant App Store.
2. Locate and install **Gemini FastAPI**.
3. Enter both cookies in the **Configuration** tab before using the App as a conversation agent.

### Step 2: Extract Authentication Cookies

1. Open a **Private/Incognito** browser window.
2. Log in to [https://gemini.google.com](https://gemini.google.com) with your secondary Google account.
3. Open **Developer Tools** (F12 or Right-click > Inspect).
4. Navigate to the **Application** tab (Chrome/Edge) or **Storage** tab (Firefox).
5. Under **Cookies**, select `https://gemini.google.com` and locate the following values:
   - `__Secure-1PSID`
   - `__Secure-1PSIDTS`
6. **Close the incognito window immediately** after copying to prevent session conflicts.

### Step 3: App Configuration

1. Open the **Gemini FastAPI** App and go to the **Configuration** tab.
2. Under **Gemini accounts**, paste the extracted values into the first account:
   - **Secure 1PSID cookie** (required): `__Secure-1PSID`
   - **Secure 1PSIDTS cookie** (required): `__Secure-1PSIDTS`
3. **(Optional)** To use more than one Google account, click **Add** under **Gemini accounts** and enter the cookies for the next account.
4. **(Recommended)** Secure your API endpoint by entering an **API key**.
5. Leave the other options at their defaults unless you need to troubleshoot.
6. Click **Save**.

> [!NOTE]
> An account needs **both** cookies. If only one is filled in, the App stops with a clear error. If no account is configured at all, the App starts in **guest mode**: it can answer text prompts, but it has no conversation history, no file uploads, and no model choice.

> [!IMPORTANT]
> Configuration is managed only from the **Configuration** tab. The App uses the upstream default `config/config.yaml` shipped inside its image and no longer creates, copies, or merges a configuration file in `/homeassistant/gemini-fastapi/config`. Only the options listed below are configurable; all other upstream settings use their defaults. On the first start after updating, the App removes the old `/homeassistant/gemini-fastapi/config` folder and moves the old `/homeassistant/gemini-fastapi/data` into its own `/data` storage. If no account is configured yet, the App starts in guest mode: enter your cookies and API key in the Configuration tab and restart it. `/homeassistant` is still mounted for this one-time migration and will be removed in a future release. If the folder is unavailable, the App still starts and retries the migration on a later start.

### Step 4: Deployment

1. Return to the Gemini FastAPI App page and click **Start**.
2. Review the **Log** tab to verify successful service initialization.

### Configuration Options

| Option      | Default           | Description                                                                                                                                      |
| ----------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `api_key`   | empty             | Optional token that API clients must send. Leave empty to disable authentication.                                                                |
| `log_level` | `debug`           | App logging level: `debug`, `info`, `warning`, `error`, or `critical`.                                                                           |
| `clients`   | one empty account | List of Gemini accounts. Each entry needs both cookies and can set an optional client ID and proxy. With no account, the App runs in guest mode. |

#### Gemini Account Fields

| Field            | Description                                                                                                                                    |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`             | Optional. Leave empty to derive a stable ID from the account cookie. Set an explicit ID if you want a readable name or need to pin an account. |
| `secure_1psid`   | **Required** together with `secure_1psidts`. The `__Secure-1PSID` cookie from `gemini.google.com`.                                             |
| `secure_1psidts` | **Required** together with `secure_1psid`. The `__Secure-1PSIDTS` cookie from `gemini.google.com`.                                             |
| `proxy`          | Optional proxy for this account, for example `socks5://127.0.0.1:1080`. Leave empty for a direct connection.                                   |

### Multiple Gemini Accounts

Each entry under **Gemini accounts** is applied as a separate upstream Gemini client. Requests are distributed across all configured accounts, which reduces per-account rate limits.

- An account needs both the `__Secure-1PSID` and `__Secure-1PSIDTS` cookies. An entry with only one of them is rejected with a clear error.
- If no account is configured, the App starts in guest mode without reusing cookies cached for a previous account. Guest sessions can answer text prompts, but they have no conversation history, no file uploads, and no model choice.
- Upstream initializes accounts one at a time, so each additional account adds a startup delay of up to 30 seconds.
- Automatically generated client IDs are derived from the `__Secure-1PSID` cookie, so adding, removing, or reordering accounts does not reassign existing conversation history. Rotating only `1PSIDTS` keeps the ID; rotating `1PSID` changes it, so set an explicit `id` if you need history to survive that.
- Set an explicit `id` if you want a readable name or need to pin an account across cookie changes.
- If you are upgrading and want to continue a conversation stored under an old client ID (for example `client-id-1`), set that `id` explicitly on the account.
- Use a different **Proxy URL** per account when the accounts should connect through different proxies.

---

## Home Assistant Integration

To utilize Gemini as a conversation agent, we recommend the [**Local OpenAI LLM**](https://github.com/luuquangvu/hass_local_openai_llm) integration.

1. **Install via HACS**:
   [![Open HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=luuquangvu&repository=hass_local_openai_llm&category=integration)
2. **Add the Integration**: Navigate to **Settings > Devices & Services** and search for "Local OpenAI LLM".
3. **Connection Settings**:
   - **Base URL**: `http://YOUR_HA_IP:8000/v1` (or `http://127.0.0.1:8000/v1` if running on the same host)
   - **API Key**: The `api_key` from the App's **Configuration** tab.

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

> [!TIP]
> For multiple Gemini accounts, repeat the client variables with contiguous indexes: `CONFIG_GEMINI__CLIENTS__0__...`, `CONFIG_GEMINI__CLIENTS__1__...`, and so on.

---

## Troubleshooting

- **Authentication Failure**: If the log indicates initialization failure, your session cookies may have expired. Please repeat the extraction process. Both the `__Secure-1PSID` and `__Secure-1PSIDTS` cookies are required.
- **Guest Mode**: If no account is configured, the App runs in guest mode with text prompts only. Enter both cookies in the **Configuration** tab to enable conversation history, file uploads, and model selection.
- **Connection Issues**: Verify that port `8000` is accessible and the `api_key` option matches your Home Assistant configuration.
- **Session Stability**: If cookies expire frequently, use Firefox to extract cookies. Recent versions of Chromium-based browsers use "Device Bound Session Credentials", which improves security but causes cookies to remain valid for only a few hours and prevents them from being renewed.

---

## Credits

- Built upon the excellent Gemini-API project from [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API).
