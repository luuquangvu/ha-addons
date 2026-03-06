# Home Assistant AI & Apps Repository - Free Gemini Integration

[🇻🇳 Tiếng Việt](README.vi.md)

[![License](https://img.shields.io/github/license/luuquangvu/ha-addons)](LICENSE)

Enhance your smart home with **Google Gemini for Home Assistant** and other AI-powered tools. This repository provides custom Apps (formerly known as add-ons) designed to bring cutting-edge AI features, experimental automations, and advanced integrations to your Home Assistant ecosystem.

## Repository Contents

- **Gemini FastAPI (Google Gemini for Home Assistant)**
  - Integrate **Google Gemini** into your smart home for free. This is an OpenAI-compatible wrapper that uses browser cookies, eliminating the need for paid API keys. It enables unlimited AI chat, conversation history, and web-grounded answers via Google Search directly within Home Assistant Assist.
  - Docs: [gemini-fastapi/README.md](gemini-fastapi/README.md)

## Installation (App Store)

You can add this repository to your Home Assistant instance using one of the following methods:

### 1. Automatic Method (Recommended)

The easiest way to add this repository is to click the button below, which will guide you through the process automatically:

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Fha-addons)

### 2. Manual Method

If the automatic method does not work, you can add the repository manually by following these steps:

1. In Home Assistant, navigate to **Settings > Apps > App Store**.
2. Click the **three-dots menu** (⋮) in the top-right corner and select **Repositories**.
3. Copy and paste the repository URL: `https://github.com/luuquangvu/ha-addons`
4. Click **Add** and then **Close** the dialog.
5. The repository's Apps will now be available in the store for installation.

> [!TIP]
> After installing an App, click **Start** once so the default configuration files are generated before editing.

## Updating / Removing

- Home Assistant automatically checks this repository for updates. You can also press the **Reload** button in the App Store to fetch the latest versions on demand.
- To remove the repository, open the **Repositories** dialog again, highlight `luuquangvu/ha-addons`, and click **Remove**. Installed Apps remain until you uninstall them.

## Support & Contributions

- Found a bug, have an idea, or want to contribute? [Open an issue](https://github.com/luuquangvu/ha-addons/issues) or submit a pull request.
- Gemini FastAPI is based on the outstanding work from [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API).

## License

Released under the MIT License. See the [LICENSE](LICENSE) file for details.
