# Home Assistant add-ons

Collection of custom Home Assistant add-ons.

## Available add-ons

### Gemini FastAPI

- Wraps the Gemini-FastAPI service into an add-on, exposing an OpenAI-compatible router backed by Google Gemini via browser cookies.
- Persists configuration and conversation data in Home Assistant storage so Gemini sessions survive container restarts and work with OpenAI-compatible clients.
- Setup guide: see [`gemini-fastapi/README.md`](gemini-fastapi/README.md).

## How to use

1. In Home Assistant, open _Settings_ > _Add-ons_ > _Add-on Store_.
2. Click the three dots menu > _Repositories_ and add: `https://github.com/luuquangvu/ha-addons`.
3. Install the desired add-on and start it from the Add-on Panel.

## Contributing & feedback

- Open an issue or pull request for bugs, feature requests, or questions.
- The catalog will expand with additional add-ons over time, stay tuned.
- Gemini FastAPI upstream project: [Nativu5/Gemini-FastAPI](https://github.com/Nativu5/Gemini-FastAPI).
