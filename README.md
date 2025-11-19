# Home Assistant Add-ons Repository

[![License](https://img.shields.io/github/license/luuquangvu/ha-addons)](LICENSE)

A collection of custom Home Assistant add-ons.

## Installation

1. Navigate to **Settings** > **Add-ons** > **Add-on Store** in your Home Assistant instance.
2. Click the three-dots menu in the top right and select **Repositories**.
3. Add the following URL: `https://github.com/luuquangvu/ha-addons`
4. Close the dialog. The new add-ons will now appear in the store.

## Available Add-ons

### Gemini FastAPI

Exposes an OpenAI-compatible API for Google Gemini.

- **Authentication**: Uses only browser cookies (`__Secure-1PSID` and `__Secure-1PSIDTS`), no Google API key required.
- **Persistence**: Automatically saves conversation history and survives restarts.
- **Upstream Project**: Based on the excellent [Nativu5/Gemini-FastAPI](https://github.com/Nativu5/Gemini-FastAPI).

> [!NOTE]
> For complete setup and configuration instructions, please see the [**Gemini FastAPI Add-on Guide**](gemini-fastapi/README.md).

## Contributing

Contributions are welcome! If you have any bugs, feature requests, or questions, please [open an issue](https://github.com/luuquangvu/ha-addons/issues) or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
