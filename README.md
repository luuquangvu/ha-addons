# Advanced AI for Home Assistant

[![Home Assistant App](https://img.shields.io/badge/Home%20Assistant-App-blue?style=for-the-badge&logo=home-assistant)](https://github.com/luuquangvu/ha-addons)

**🇺🇸 English | [🇻🇳 Tiếng Việt](README.vi.md)**

Integrate advanced AI capabilities into your Home Assistant instance. This repository provides specialized Apps designed to bring state-of-the-art Generative AI, local voice processing (STT & TTS), intelligent automations, and advanced integrations to your smart home ecosystem.

## Repository Contents

- **Google Gemini for Home Assistant (Gemini FastAPI)**
  - Integrate **Google Gemini** into your smart home for free. This OpenAI-compatible API bridge uses browser session cookies, eliminating the need for Google Cloud API keys. It enables conversation history, multimodal processing, and real-time answers via Google Search directly within Home Assistant Assist.
  - **📖 Detailed Documentation:** [Read the full guide here →](gemini-fastapi/README.md)

- **Vietnamese Voice for Home Assistant (Wyoming Vietnamese)**
  - Give Assist a Vietnamese voice that runs entirely on your own hardware. This App serves both speech-to-text and text-to-speech over a single Wyoming Protocol port, with 20 Vietnamese voices, no cloud account, and no API key.
  - **📖 Detailed Documentation:** [Read the full guide here →](wyoming-vietnamese/README.md)

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
> Configuration and first-start behavior depend on the App (e.g., **Gemini FastAPI** generates default configuration files on initial launch, while **Wyoming Vietnamese** downloads speech and voice models on its first run). Please consult each App's individual documentation for specific instructions.

## Maintenance

- **Updates**: Home Assistant periodically checks for updates. You can also manually refresh the store using the **Reload** button.
- **Removal**: To remove the repository, go to the **Repositories** dialog, select `luuquangvu/ha-addons`, and click **Remove**. Installed Apps will remain until uninstalled manually.

---

## Support & Credits

- **Support**: Report issues or contribute via [GitHub Issues](https://github.com/luuquangvu/ha-addons/issues).
- **Credits**:
  - **Gemini FastAPI**: Built upon the [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API) project.
  - **Wyoming Vietnamese**: Powered by models and libraries from [nghimestudio/nghitts](https://github.com/nghimestudio/nghitts), [hynt](https://huggingface.co/hynt), [k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx), and the [Wyoming Protocol](https://github.com/OHF-Voice/wyoming).

## License

MIT License. See [LICENSE](LICENSE) for details.
