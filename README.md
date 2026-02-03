# Home Assistant Add-ons Repository

[🇻🇳 Tiếng Việt](README.vi.md)

[![License](https://img.shields.io/github/license/luuquangvu/ha-addons)](LICENSE)

Custom add-ons that enhance Home Assistant with AI features and other experimental ideas. Every add-on lives in its own folder with documentation, configuration, and icon assets, so you can pick only what you need.

## Repository Contents

- **Gemini FastAPI**
  - An OpenAI-compatible wrapper for Google Gemini that works with browser cookies, eliminating the need for an official API key, allowing completely free and unlimited use. It features conversation persistence, Google Search integration, and optional API key protection. Docker users can easily follow the standalone deployment instructions provided in the guide.
  - Docs: [gemini-fastapi/README.md](gemini-fastapi/README.md)

## Installation (Add-on Store)

You can add this repository to your Home Assistant instance using one of the following methods:

### 1. Automatic Method (Recommended)

The easiest way to add this repository is to click the button below, which will guide you through the process automatically:

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Fha-addons)

### 2. Manual Method

If the automatic method does not work, you can add the repository manually by following these steps:

1. In Home Assistant, navigate to **Settings > Add-ons > Add-on Store**.
2. Click the **three-dots menu** (⋮) in the top-right corner and select **Repositories**.
3. Copy and paste the repository URL: `https://github.com/luuquangvu/ha-addons`
4. Click **Add** and then **Close** the dialog.
5. The repository's add-ons will now be available in the store for installation.

> [!TIP]
> After installing an add-on, click **Start** once so the default configuration files are generated before editing.

## Updating / Removing

- Home Assistant automatically checks this repository for updates. You can also press the **Reload** button in the Add-on Store to fetch the latest versions on demand.
- To remove the repository, open the **Repositories** dialog again, highlight `luuquangvu/ha-addons`, and click **Remove**. Installed add-ons remain until you uninstall them.

## Support & Contributions

- Found a bug, have an idea, or want to contribute? [Open an issue](https://github.com/luuquangvu/ha-addons/issues) or submit a pull request.
- Gemini FastAPI is based on the outstanding work from [Nativu5/Gemini-FastAPI](https://github.com/Nativu5/Gemini-FastAPI).

## License

Released under the MIT License. See the [LICENSE](LICENSE) file for details.
