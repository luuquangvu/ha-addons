# Wyoming Vietnamese for Home Assistant

[![Home Assistant App](https://img.shields.io/badge/Home%20Assistant-Add--on-blue?style=for-the-badge&logo=home-assistant)](https://github.com/luuquangvu/ha-addons)

**🇺🇸 English | [🇻🇳 Tiếng Việt](README.vi.md)**

Let Home Assistant Assist listen and answer in natural Vietnamese, entirely inside your own network. This App bundles Vietnamese **speech-to-text (STT)** and **text-to-speech (TTS)** into a single Wyoming Protocol service, so Home Assistant only needs one host and one port.

> [!NOTE]
> This App packages the [Wyoming Vietnamese](https://github.com/luuquangvu/wyoming-vietnamese) service image for Home Assistant, with model storage kept in the App's persistent `/data` volume.

---

## Technical Features

- **Combined STT and TTS**: Both services are advertised on the shared Wyoming port `10300`.
- **Fully Local**: No cloud account and no API key. Audio and text are not sent to a third-party service during use.
- **19 Vietnamese Voices**: Select one or more voices; the first one configured is the default in Assist.
- **Persistent Models**: Models are downloaded once into the App's `/data` storage, so later restarts are fast.
- **Offline Mode**: Once every model is cached, the service can run without any Internet access.
- **Natural Pacing**: Sentence and clause pauses, plus a random jitter, are configurable to avoid robotic delivery.

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
> Changing an option requires **restarting** the App. Options are applied at process start.

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

| Option                       | Default                     | Description                                                                                       |
| ---------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------- |
| `tts_voice`                  | `ngoc-huyen-moi, ngoc-ngan` | One or more voice IDs separated by commas and/or spaces. The first one is the default voice.      |
| `cpu_threads`                | `0`                         | Inference threads. `0` auto-detects the available CPU threads.                                    |
| `offline`                    | `false`                     | Set to `true` only after every model has been downloaded. Startup then fails instead of fetching. |
| `tts_sentence_silence_ms`    | `400`                       | Pause between sentences and lines, in milliseconds. Raise it for slower reading.                  |
| `tts_clause_silence_ms`      | `180`                       | Pause after commas and other clause punctuation, in milliseconds.                                 |
| `tts_silence_jitter_percent` | `25`                        | Random +/- spread applied to each pause so delivery sounds less robotic.                          |
| `log_level`                  | `info`                      | Use `debug` for detailed logs while troubleshooting.                                              |

### Available Voices

| ID                     | Display name         |
| ---------------------- | -------------------- |
| `ban-mai`              | Ban Mai              |
| `chieu-thanh`          | Chiếu Thành          |
| `duy-onyx-moi`         | Duy Onyx (mới)       |
| `duy-oryx`             | Duy Oryx             |
| `lac-phi`              | Lạc Phi              |
| `mai-phuong`           | Mai Phương           |
| `minh-khang`           | Minh Khang           |
| `minh-quang`           | Minh Quang           |
| `manh-dung`            | Mạnh Dũng            |
| `my-tam`               | Mỹ Tâm               |
| `my-tam-real`          | Mỹ Tâm Real          |
| `ngoc-huyen-moi`       | Ngọc Huyền (mới)     |
| `ngoc-ngan`            | Ngọc Ngạn            |
| `phuong-trang`         | Phương Trang         |
| `thanh-phuong-viettel` | Thanh Phương Viettel |
| `thien-tam`            | Thiện Tâm            |
| `tran-thanh`           | Trấn Thành           |
| `tai-an`               | Tài An               |
| `viet-thao`            | Việt Thảo            |

Each additional voice is downloaded and kept loaded in memory, so select only the voices you actually use.

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
      - "TZ=Asia/Ho_Chi_Minh"
      - "TTS_VOICE=ngoc-huyen-moi, ngoc-ngan"
      - "CPU_THREADS=0"
      - "OFFLINE=false"
      - "LOG_LEVEL=info"
    volumes:
      - cache:/app/.cache
      - models:/app/models

volumes:
  cache:
  models:
```

### Docker CLI

```bash
docker run -d --name wyoming-vietnamese \
  --restart unless-stopped \
  -p 10300:10300 \
  -e "TTS_VOICE=ngoc-huyen-moi, ngoc-ngan" \
  -e "LOG_LEVEL=info" \
  -v wyoming-vietnamese-cache:/app/.cache \
  -v wyoming-vietnamese-models:/app/models \
  ghcr.io/luuquangvu/wyoming-vietnamese:latest
```

---

## Troubleshooting

- **Wyoming cannot be added in Home Assistant**: Confirm the App is running and that port `10300` is reachable. Check the **Log** tab for startup errors.
- **The App stays busy on first start**: The STT model and each voice are downloaded on the first start. Keep the Internet connection available until the log reports that the service is ready.
- **Startup fails with `offline` enabled**: Set `offline` back to `false`, restart, and wait for the download to finish before enabling it again.
- **Home Assistant still uses the old voice**: Verify the voice ID against the table above, restart the App, then reload the Voice assistants page.
- **Speech sounds rushed**: Increase `tts_sentence_silence_ms` and `tts_clause_silence_ms`.

---

## Credits

- [nghimestudio/nghitts](https://github.com/nghimestudio/nghitts) for the Vietnamese voice models.
- [hynt](https://huggingface.co/hynt) for the `Zipformer-30M-RNNT-6000h` recognition model.
- [k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) for the STT and TTS inference engines.
- [Wyoming Protocol](https://github.com/OHF-Voice/wyoming) for the Home Assistant Voice integration layer.
