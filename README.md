# Advanced AI for Home Assistant - Google Gemini & Intelligent Tools

[![Home Assistant App](https://img.shields.io/badge/Home%20Assistant-App-blue?style=for-the-badge&logo=home-assistant)](https://github.com/luuquangvu/ha-addons)

**[ 🇺🇸 English | [🇻🇳 Tiếng Việt](README.vi.md) ]**

Integrate advanced AI capabilities into your Home Assistant instance. This repository provides specialized Apps designed to bring state-of-the-art Generative AI, intelligent automations, and advanced integrations to your smart home ecosystem.

## Repository Contents

- **Google Gemini for Home Assistant (Gemini FastAPI)**
  - Integrate **Google Gemini** into your smart home for free. This OpenAI-compatible API bridge uses browser session cookies, eliminating the need for Google Cloud API keys. It enables conversation history, multimodal processing, and real-time answers via Google Search directly within Home Assistant Assist.
  - **📖 Detailed Documentation:** [Read the full guide here →](gemini-fastapi/README.md)

## Installation Guide

Add this repository to your Home Assistant instance using one of the following methods:

### 1. Automatic Method (Recommended)

Click the button below to automatically add the repository to your Assistant:

[![Open your Home Assistant instance and show the add App Store repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Fha-addons)

### 2. Manual Method

1. In Home Assistant, navigate to **Settings > Apps > App Store**.
2. Click the **three-dots menu** (⋮) in the top-right corner and select **Repositories**.
3. Add the repository URL: `https://github.com/luuquangvu/ha-addons`
4. Click **Add** and then **Close**.
5. The available Apps will now appear in the store for installation.

> [!TIP]
> After installing an App, **Start** it once to generate default configuration files before editing the settings.

## Maintenance

- **Updates**: Home Assistant periodically checks for updates. You can also manually refresh the store using the **Reload** button.
- **Removal**: To remove the repository, go to the **Repositories** dialog, select `luuquangvu/ha-addons`, and click **Remove**. Installed Apps will remain until uninstalled manually.

---

## Support & Credits

- Report issues or contribute via [GitHub Issues](https://github.com/luuquangvu/ha-addons/issues).
- Gemini FastAPI is built upon the library from [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API).

## License

MIT License. See [LICENSE](LICENSE) for details.
