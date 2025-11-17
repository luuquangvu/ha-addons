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

4. Save the file and restart the add-on from the Add-on panel.

The add-on persists configuration under `/homeassistant/gemini-fastapi/config` and stores conversation data under `/homeassistant/gemini-fastapi/data`, keeping credentials and history across restarts. On updates, a refreshed template is written to `/homeassistant/gemini-fastapi/config/config.yaml.default` so you can compare it with your existing configuration.

### How to obtain Gemini cookies

1. Open an incognito/private window and visit [https://gemini.google.com](https://gemini.google.com), then sign in.
2. Open your browser's developer tools (usually `F12`) and switch to the **Application** tab.
3. Locate the **Storage** > **Cookies** section for `https://gemini.google.com`.
4. Copy the values of `__Secure-1PSID` and `__Secure-1PSIDTS` and paste them into your configuration.

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

## Upstream documentation

Refer to the official project README for advanced settings and authentication details: [https://github.com/Nativu5/Gemini-FastAPI](https://github.com/Nativu5/Gemini-FastAPI).
