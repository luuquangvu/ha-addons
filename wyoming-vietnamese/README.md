# Wyoming Vietnamese for Home Assistant

[![Home Assistant App](https://img.shields.io/badge/Home%20Assistant-Add--on-blue?style=for-the-badge&logo=home-assistant)](https://github.com/luuquangvu/ha-addons)

**🇺🇸 English | [🇻🇳 Tiếng Việt](README.vi.md)**

Let Home Assistant Assist listen and answer in natural Vietnamese, entirely inside your own network. This App bundles Vietnamese **speech-to-text (STT)** and **text-to-speech (TTS)** into a single Wyoming Protocol service, so Home Assistant only needs one host and one port.

> [!NOTE]
> This App packages the [Wyoming Vietnamese](https://github.com/luuquangvu/wyoming-vietnamese) service image for Home Assistant, with model storage kept in the App's persistent `/data` volume.

---

## Technical Features

- **All-in-One STT & TTS**: Combines both speech-to-text and text-to-speech over a single Wyoming Protocol port (`10300`), saving system resources and simplifying Home Assistant configuration.
- **100% Local & Privacy First**: All voice commands, recognition, and smart home responses are processed locally without cloud dependencies, API fees, or external data transmission.
- **Dual Next-Gen TTS Engines**:
  - **NghiTTS Engine (`tts_engine: nghitts`)**: Built on the VITS architecture (22.05 kHz) powered by the highly optimized C++ `sherpa-onnx` runtime. Sub-second response latency (< 0.2s) with minimal resource consumption, ideal for Raspberry Pi 4/5 and low-power hardware.
  - **ZeroTTS Engine (`tts_engine: zerotts`)**: Utilizes the ZeroTTS neural speech language model (GGUF Q8_0 format) with MOSS Audio Codec 48 kHz via C++ GGML runtime. Delivers studio-grade audio quality, vivid expression, and human-like natural phrasing.
- **Rich Library of 28 Voices**: 20 NghiTTS voices and 8 ZeroTTS voices covering Northern, Central, and Southern accents, male and female, suited for voice assistants, news broadcasters, narrators, and audiobooks.
- **Natural Grammar-Aware Pacing**: Automatically detects sentence and clause boundaries (periods, commas, colons) and paragraph breaks to apply appropriate pauses, ensuring smooth, fluent delivery.
- **Persistent Model Storage & Offline Ready**: Automatically downloads and verifies models (SHA-256) on first start into persistent `/data` storage, ready for long-term offline operation without an ongoing Internet connection.

---

## Quick Comparison: TTS Engines

| Criteria                  | NghiTTS Engine (`nghitts` - Default)                  | ZeroTTS Engine (`zerotts`)                                                        |
| :------------------------ | :---------------------------------------------------- | :-------------------------------------------------------------------------------- |
| **Core Architecture**     | VITS via C++ runtime `sherpa-onnx`                    | Neural Transformer (GGUF Q8_0) + MOSS Codec via C++ runtime GGML                  |
| **Audio Quality**         | 22.05 kHz (clear, crisp, easy to understand)          | 48 kHz (studio-grade audio, high detail)                                          |
| **Latency**               | Ultra-fast (< 0.2s), near-instant response            | Smooth (~0.5s - 1.5s depending on CPU performance)                                |
| **Voice Characteristics** | Clear, crisp, standard voice assistant & news style   | Highly natural, expressive, authentic human-like intonation and pacing            |
| **Hardware Requirements** | Very light (ideal for Raspberry Pi 4/5, Mini PC, NAS) | Moderate CPU required (recommended x86 Mini PC: Intel N100, Core i, AMD Ryzen...) |
| **Available Voices**      | 20 voices (Northern, Central, Southern)               | 8 voices (Northern)                                                               |

---

## Installation and Configuration

### Step 1: App Installation

1. Add the [**luuquangvu/ha-addons**](https://github.com/luuquangvu/ha-addons) repository to your Home Assistant App Store.
2. Locate and install **Wyoming Vietnamese**.
3. Open the **Configuration** tab and adjust the options below if needed.

### Step 2: First Start

1. Click **Start**. The first start needs Internet access and may take several minutes while the STT model and the selected voices are downloaded.
2. Watch the **Log** tab until the service reports that it is ready.

> [!IMPORTANT]
> Changing an option requires **restarting** the App. Options are applied at process start. After changing `tts_engine`, the **Wyoming Protocol** integration in Home Assistant must also be **reloaded** (**Settings > Devices & Services > Wyoming Protocol > ⋮ > Reload**) to take effect and update the voice catalog.

### Step 3: Home Assistant Integration

1. Go to **Settings > Devices & Services**.
2. Click **Add Integration** and search for **Wyoming Protocol**.
3. Enter the host running Home Assistant (for example `homeassistant.local` or the host IP) and port `10300`.
4. Go to **Settings > Voice assistants**, open your Assist pipeline, and select Wyoming Vietnamese for both **Speech-to-text** and **Text-to-speech**.

### Step 4: Watchdog (Optional)

The App page has a **Watchdog** toggle that restarts the service whenever it stops answering on port `10300`.

Leave it **off** until the first start has finished downloading. The port is opened only after every model is loaded, so an armed watchdog can interrupt a long first download. Once Assist is working, turn it on to recover automatically from a stalled service.

---

## Configuration Options

> [!NOTE]
> After changing `tts_engine`, restart the App and **reload** the **Wyoming Protocol** integration in Home Assistant (**Settings > Devices & Services > Wyoming Protocol > ⋮ > Reload**) so Home Assistant updates the voice catalog and applies the new engine.
>
> For low-end devices (e.g., Raspberry Pi or hardware with limited resources), choose `nghitts` with only **1 voice** in `tts_voice` (e.g., `ngoc-huyen-moi`) to reduce CPU/RAM usage and ensure the smoothest performance.

| Option       | Default                                                                     | Description                                                                                                                    |
| ------------ | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `tts_engine` | `nghitts`                                                                   | TTS engine to use: `nghitts` (NghiTTS via sherpa-onnx) or `zerotts` (ZeroTTS via GGML).                                        |
| `tts_voice`  | `ngoc-huyen-moi, duy-onyx-moi, thanh-phuong-viettel, ngoc-ngan, mai-phuong` | One or more voice IDs separated by commas and/or spaces for the selected engine. The first one is the default voice in Assist. |
| `log_level`  | `info`                                                                      | Use `debug` for detailed logs while troubleshooting.                                                                           |

### Available Voices

#### NghiTTS Voices (VITS 22.05 kHz)

| Voice ID (`id`)        | Display Name         | Region / Characteristics                                                                  |
| :--------------------- | :------------------- | :---------------------------------------------------------------------------------------- |
| `ngoc-huyen-moi`       | Ngọc Huyền (mới)     | Northern Female (crisp, natural, ideal for daily assistant, reviews & news)               |
| `ban-mai`              | Ban Mai              | Northern Female (gentle, broadcaster style, highly expressive)                            |
| `thanh-phuong-viettel` | Thanh Phương Viettel | Northern Female (clear, articulate, decisive, professional assistant & call center style) |
| `mai-phuong`           | Mai Phương           | Northern Female (soft, warm, suitable for audiobooks and long news)                       |
| `phuong-trang`         | Phương Trang         | Northern Female (deep, warm, expressive, narration & documentary style)                   |
| `duy-onyx-moi`         | Duy Onyx (mới)       | Northern Male (deep, warm, modern, natural intonation, ideal male assistant)              |
| `duy-oryx`             | Duy Oryx             | Northern Male (deep, poised and steady)                                                   |
| `minh-khang`           | Minh Khang           | Northern Male (youthful, energetic, engaging, "Kiến Giải Mã" explanation style)           |
| `minh-quang`           | Minh Quang           | Northern Male (mature, articulate, news broadcast style)                                  |
| `manh-dung`            | Mạnh Dũng            | Northern Male (resonant, energetic, decisive, reportage & documentary style)              |
| `chieu-thanh`          | Chiếu Thành          | Southern Male (deep, warm, martial arts & historical storytelling style)                  |
| `thien-tam`            | Thiện Tâm            | Southern Male (calm, contemplative, serene, conversational & philosophical audio)         |
| `ngoc-ngan`            | Ngọc Ngạn            | Northern Male (deep, witty, iconic Paris By Night host style)                             |
| `tran-thanh`           | Trấn Thành           | Southern Male (eloquent, versatile, vivid and humorous entertainer style)                 |
| `viet-thao`            | Việt Thảo            | Southern Male (witty, lively, approachable, stage MC style)                               |
| `tai-an`               | Tài An               | Northern Male (crisp, articulate, CD Media historical narration style)                    |
| `lac-phi`              | Lạc Phi              | Northern Female (expressive, movie review & narration style)                              |
| `my-tam`               | Mỹ Tâm               | Central / Southern Female (warm signature tone of singer Mỹ Tâm)                          |
| `my-tam-real`          | Mỹ Tâm Real          | Central / Southern Female (signature tone of singer Mỹ Tâm, natural & authentic)          |
| `adam`                 | adam                 | International Male (ElevenLabs Adam timbre reading Vietnamese accurately)                 |

#### ZeroTTS Voices (Neural 48 kHz)

| Voice ID (`id`) | Display Name | Region / Characteristics                                                       |
| :-------------- | :----------- | :----------------------------------------------------------------------------- |
| `maichi`        | Mai Chi      | Northern Female (gentle, friendly, natural like real-life conversation)        |
| `baotrang`      | Bảo Trang    | Northern Female (mature, poised, articulate, neutral, great for news)          |
| `giahuy`        | Gia Huy      | Northern Male (young, warm, intimate, great for storytelling and dialogue)     |
| `hamy`          | Hà My        | Northern Female (young, bright high-pitch, vivid expression, energetic)        |
| `huuduc`        | Hữu Đức      | Northern Male (elderly, calm, deep and warm, traditional storytelling style)   |
| `kimoanh`       | Kim Oanh     | Northern Female (middle-aged, warm, emotionally rich, narration & story style) |
| `quangminh`     | Quang Minh   | Northern Male (young, decisive, clear, standard news anchor style)             |
| `tiendat`       | Tiến Đạt     | Northern Male (young, lively, high energy, sports commentator style)           |

Each additional voice is downloaded and kept loaded in memory, so select only the voices you actually use. On low-end devices, configure only 1 voice with `nghitts` for the smoothest performance and minimal CPU/RAM usage.

---

## Containerized Deployment (Docker)

The same service can run outside Home Assistant.

### Docker Compose

```yaml
services:
  wyoming-vietnamese:
    image: ghcr.io/luuquangvu/wyoming-vietnamese:latest
    container_name: wyoming-vietnamese
    restart: unless-stopped
    stop_grace_period: 60s
    ports:
      - "10300:10300"
    environment:
      WYOMING_PORT: 10300
      TTS_ENGINE: "nghitts"
      TTS_VOICE: "ngoc-huyen-moi, duy-onyx-moi, thanh-phuong-viettel, ngoc-ngan, mai-phuong"
      LOG_LEVEL: "info"
    volumes:
      - cache:/app/.cache
      - models:/app/models

volumes:
  cache:
  models:
```

### Docker CLI

```bash
docker run -d \
  --name wyoming-vietnamese \
  --restart unless-stopped \
  -p 10300:10300 \
  -e TTS_ENGINE="nghitts" \
  -e TTS_VOICE="ngoc-huyen-moi, duy-onyx-moi, thanh-phuong-viettel, ngoc-ngan, mai-phuong" \
  -v wyoming-vietnamese-cache:/app/.cache \
  -v wyoming-vietnamese-models:/app/models \
  ghcr.io/luuquangvu/wyoming-vietnamese:latest
```

To update to a new image or change environment variables, pull the latest image, delete the old container, and start again. Named volumes (`wyoming-vietnamese-cache` and `wyoming-vietnamese-models`) are preserved so downloaded models are not lost:

```bash
docker pull ghcr.io/luuquangvu/wyoming-vietnamese:latest
docker rm -f wyoming-vietnamese
```

### Building Docker Image from Source

For developers or advanced users wishing to customize the codebase:

```bash
git clone https://github.com/luuquangvu/wyoming-vietnamese.git
cd wyoming-vietnamese
docker compose up --build -d
```

---

## Troubleshooting

### 1. Home Assistant reports "Failed to connect" to Wyoming Protocol

- **Check App Status**: Ensure the Wyoming Vietnamese App is running and port `10300` is open.
- **Inspect Logs**: Check the **Log** tab in the App page to verify that the service printed the ready notice (`Wyoming STT/TTS service is ready at tcp://0.0.0.0:10300`).
- **Check Firewall**: Ensure port `10300` on the Home Assistant host is not blocked by a system firewall or network rule.
- **Check Host Address**: Use the correct LAN IP of the Home Assistant host (e.g. `192.168.1.100` or `homeassistant.local`), avoiding `localhost` if Home Assistant and the service reside in separated networking environments.

### 2. App takes long or exits on first start

- **Check Internet Connection**: On first start, Internet access is required to download the STT Zipformer model and configured TTS voices (typically 1 to 3 minutes depending on network speed).
- **Monitor Download Progress**: Check the **Log** tab in real-time to follow file downloads and SHA-256 integrity verification.
- **Hardware Limitations**: If the system has limited RAM (< 2 GB), select `tts_engine: nghitts` and configure only 1 or 2 essential voices to conserve memory.

### 3. Changed `tts_voice` but Home Assistant does not show new voices

- Configuration options only take effect when the App restarts. After saving and restarting the App, navigate in Home Assistant to **Settings > Devices & Services > Wyoming Protocol > ⋮ > Reload** to sync the updated voice catalog.

### 4. Audio stuttering or high latency on Raspberry Pi

- Switch to the `nghitts` engine (`tts_engine: nghitts`). It uses a lightweight VITS model optimized for ARM architectures like Raspberry Pi 4/5. The `zerotts` engine uses a significantly larger neural language model designed for servers with capable x86 CPUs.

---

## Credits

Built upon excellent open-source projects:

- [nghimestudio/nghitts](https://github.com/nghimestudio/nghitts): High-quality Vietnamese text-to-speech voice models for `nghitts`.
- [zeroweight-ai/ZeroTTS](https://github.com/zeroweight-ai/ZeroTTS): ZeroTTS neural speech language models and C++ GGML runtime for `zerotts`.
- [hynt](https://huggingface.co/hynt): Vietnamese speech-to-text recognition model `Zipformer-30M-RNNT-6000h`.
- [k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx): Highly optimized offline inference engine for STT and TTS.
- [Wyoming Protocol](https://github.com/OHF-Voice/wyoming): Open voice assistant protocol for the Home Assistant ecosystem.
