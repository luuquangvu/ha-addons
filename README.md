# Home Assistant Add-ons Repository

[![License](https://img.shields.io/github/license/luuquangvu/ha-addons)](LICENSE)

Custom add-ons that enhance Home Assistant with AI features and other experimental ideas. Every add-on lives in its own folder with documentation, configuration, and icon assets so you can pick only what you need.

## Repository Contents

- **Gemini FastAPI**  
  OpenAI-compatible wrapper for Google Gemini that works with browser cookies instead of an official API key, so you can use Gemini completely free. Includes conversation persistence, Google Search integration, and optional API key protection. Docker users can follow the standalone deployment instructions directly in the guide.  
  Docs: [gemini-fastapi/README.md](gemini-fastapi/README.md)

## Installation (Add-on Store)

1. In Home Assistant, open **Settings > Add-ons > Add-on Store**.
2. Click the three-dots menu in the top-right and select **Repositories**.
3. Paste the repository URL `https://github.com/luuquangvu/ha-addons` and click **Add**.
4. Close the dialog. All add-ons from this repo now appear inside the store and can be installed like any other add-on.

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
