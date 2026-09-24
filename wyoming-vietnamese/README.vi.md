# Wyoming Vietnamese cho Home Assistant

[![Home Assistant App](https://img.shields.io/badge/Home%20Assistant-Add--on-blue?style=for-the-badge&logo=home-assistant)](https://github.com/luuquangvu/ha-addons)

**[🇺🇸 English](README.md) | 🇻🇳 Tiếng Việt**

Giúp Assist của Home Assistant nghe và trả lời bằng tiếng Việt tự nhiên, ngay trong mạng nhà bạn. App này gói cả dịch vụ **chuyển giọng nói thành văn bản (STT)** và **chuyển văn bản thành giọng nói (TTS)** vào một dịch vụ Wyoming Protocol duy nhất, nên Home Assistant chỉ cần kết nối tới một địa chỉ và một cổng.

> [!NOTE]
> App này đóng gói ảnh dịch vụ [Wyoming Vietnamese](https://github.com/luuquangvu/wyoming-vietnamese) cho Home Assistant, với mô hình (model) được lưu trong phân vùng `/data` cố định của App.

---

## Tính năng Kỹ thuật

- **Tất cả trong một (All-in-One: STT & TTS)**: Cả hai dịch vụ nhận diện giọng nói và tổng hợp giọng đọc đều dùng chung cổng Wyoming `10300`, giúp tiết kiệm tài nguyên và tinh giản cấu hình trên Home Assistant.
- **Bảo mật và Riêng tư tuyệt đối (100% Local & Privacy)**: Mọi dữ liệu thu âm, câu lệnh điều khiển và phản hồi nhà thông minh đều được xử lý nội bộ, không phụ thuộc đám mây, không mất phí API và không gửi dữ liệu ra ngoài Internet.
- **Linh hoạt lựa chọn 2 engine TTS thế hệ mới**:
  - **Engine NghiTTS (`tts_engine: nghitts`)**: Xây dựng trên kiến trúc VITS (22.05 kHz) chạy qua runtime C++ `sherpa-onnx` tối ưu cao. Tốc độ phản hồi gần như tức thì (< 0.2s), tiêu thụ rất ít tài nguyên, lý tưởng cho Raspberry Pi 4/5 và các dòng Mini PC tiết kiệm điện.
  - **Engine ZeroTTS (`tts_engine: zerotts`)**: Sử dụng mô hình AI ngôn ngữ giọng nói ZeroTTS (định dạng GGUF Q8_0) kết hợp MOSS Audio Codec 48 kHz qua runtime C++ GGML. Chất âm chuẩn phòng thu, ngữ điệu truyền cảm và biểu cảm sống động như người thật.
- **Thư viện 28 giọng đọc phong phú**: Cung cấp sẵn 20 giọng NghiTTS và 8 giọng ZeroTTS với đầy đủ các vùng miền Bắc - Trung - Nam, giọng nam, giọng nữ, đa dạng phong cách từ trợ lý ảo, phát thanh viên, MC cho đến đọc truyện, tâm sự.
- **Xử lý ngắt nghỉ tự nhiên theo ngữ pháp**: Thuật toán tự động nhận diện cấu trúc câu (dấu chấm, phẩy, hai chấm...) và các đoạn văn để căn chỉnh khoảng lặng hợp lý, giúp câu thoại liền mạch, lưu loát, không bị dồn chữ hay cảm giác "đọc như máy".
- **Lưu trữ mô hình cố định & Chạy offline**: Tự động tải và kiểm tra toàn vẹn (checksum SHA-256) các mô hình ở lần khởi chạy đầu vào phân vùng `/data` của App, sẵn sàng vận hành lâu dài mà không cần duy trì kết nối Internet.

---

## So sánh nhanh 2 engine TTS

| Tiêu chí                      | Engine NghiTTS (`nghitts` - Mặc định)                             | Engine ZeroTTS (`zerotts`)                                                           |
| :---------------------------- | :---------------------------------------------------------------- | :----------------------------------------------------------------------------------- |
| **Kiến trúc cốt lõi**         | VITS qua runtime C++ `sherpa-onnx`                                | Neural Transformer (GGUF Q8_0) + MOSS Codec qua runtime C++ GGML                     |
| **Chất lượng âm thanh**       | 22.05 kHz (rõ ràng, mạch lạc, dễ nghe)                            | 48 kHz (chất lượng âm thanh phòng thu, chi tiết cao)                                 |
| **Tốc độ phản hồi (Latency)** | Siêu nhanh (< 0.2 giây), phản hồi gần như tức thì                 | Mượt mà (khoảng 0.5 đến 1.5 giây tùy hiệu năng CPU)                                  |
| **Đặc trưng giọng đọc**       | Rõ ràng, dứt khoát, chuẩn phong cách trợ lý ảo và phát thanh viên | Rất tự nhiên, giàu cảm xúc, nhấn nhá và ngữ điệu chân thực như người thật            |
| **Yêu cầu phần cứng**         | Rất nhẹ (phù hợp Raspberry Pi 4/5, Mini PC, NAS)                  | Yêu cầu CPU tương đối (khuyên dùng Mini PC x86 như Intel N100, Core i, AMD Ryzen...) |
| **Số lượng giọng đọc**        | 20 giọng (Bắc, Trung, Nam)                                        | 8 giọng (Bắc)                                                                        |

---

## Hướng dẫn Cài đặt và Cấu hình

### Bước 1: Cài đặt App

1. Thêm kho lưu trữ [**luuquangvu/ha-addons**](https://github.com/luuquangvu/ha-addons) vào Cửa hàng App của Home Assistant.
2. Tìm và cài đặt **Wyoming Vietnamese**.
3. Mở tab **Configuration** (Cấu hình) và điều chỉnh các tùy chọn bên dưới nếu cần.

### Bước 2: Khởi động lần đầu

1. Nhấn **Start**. Lần khởi động đầu tiên cần Internet và có thể mất vài phút để tải mô hình STT cùng các giọng đã chọn.
2. Theo dõi tab **Log** cho tới khi dịch vụ báo đã sẵn sàng.

> [!IMPORTANT]
> Sau khi thay đổi tùy chọn, hãy **khởi động lại (Restart)** App. Các tùy chọn chỉ được đọc khi tiến trình khởi động. Sau khi đổi `tts_engine`, bạn cần **tải lại (Reload)** tích hợp **Wyoming Protocol** trong Home Assistant (**Cài đặt > Thiết bị & dịch vụ > Wyoming Protocol > ⋮ > Tải lại**) để áp dụng engine mới và cập nhật danh sách giọng đọc.

### Bước 3: Tích hợp với Home Assistant

1. Mở **Cài đặt > Thiết bị & dịch vụ**.
2. Chọn **Thêm tích hợp** và tìm **Wyoming Protocol**.
3. Nhập địa chỉ máy đang chạy Home Assistant (ví dụ `homeassistant.local` hoặc IP của máy) và cổng `10300`.
4. Mở **Cài đặt > Trợ lý giọng nói**, chọn chuỗi xử lý (pipeline) Assist của bạn và đặt Wyoming Vietnamese cho cả **Speech-to-text** lẫn **Text-to-speech**.

### Bước 4: Watchdog (Tùy chọn)

Trang App có công tắc **Watchdog** giúp tự động khởi động lại dịch vụ mỗi khi cổng `10300` ngừng phản hồi.

Hãy để **tắt** cho tới khi lần khởi động đầu tiên tải xong mô hình. Cổng chỉ được mở sau khi mọi mô hình đã được nạp, nên watchdog đang bật có thể làm gián đoạn quá trình tải lần đầu vốn khá lâu. Khi Assist đã hoạt động, hãy bật công tắc này để dịch vụ tự phục hồi nếu bị treo.

---

## Các Tùy chọn Cấu hình

> [!NOTE]
> Sau khi đổi `tts_engine`, hãy khởi động lại App và **tải lại (Reload)** tích hợp **Wyoming Protocol** trong Home Assistant (**Cài đặt > Thiết bị & dịch vụ > Wyoming Protocol > ⋮ > Tải lại**) để thay đổi và danh sách giọng đọc có hiệu lực.
>
> Đối với thiết bị cấu hình thấp (như Raspberry Pi hoặc phần cứng tiết kiệm điện), khuyến nghị chọn `tts_engine: nghitts` và chỉ cấu hình duy nhất **1 giọng đọc** trong `tts_voice` (ví dụ: `ngoc-huyen-moi`) để giảm tải RAM/CPU và giúp hệ thống hoạt động mượt mà nhất.

| Tùy chọn     | Mặc định                                                                    | Mô tả                                                                                                                                 |
| ------------ | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `tts_engine` | `nghitts`                                                                   | Engine phát giọng đọc: `nghitts` (NghiTTS qua sherpa-onnx) hoặc `zerotts` (ZeroTTS qua GGML).                                         |
| `tts_voice`  | `ngoc-huyen-moi, duy-onyx-moi, thanh-phuong-viettel, ngoc-ngan, mai-phuong` | Một hoặc nhiều mã giọng của engine đã chọn, ngăn cách bằng dấu phẩy và/hoặc khoảng trắng. Mã đầu tiên là giọng mặc định trong Assist. |
| `log_level`  | `info`                                                                      | Đặt `debug` khi cần xem nhật ký chi tiết để chẩn đoán sự cố.                                                                          |

### Các giọng có sẵn

#### Bảng mã giọng đọc engine NghiTTS (VITS 22.05 kHz)

| Mã giọng (`id`)        | Tên hiển thị         | Vùng miền / Đặc trưng phong cách                                                                 |
| :--------------------- | :------------------- | :----------------------------------------------------------------------------------------------- |
| `ngoc-huyen-moi`       | Ngọc Huyền (mới)     | Nữ miền Bắc (trong trẻo, tự nhiên, thích hợp làm trợ lý hàng ngày, đọc review và tin tức)        |
| `ban-mai`              | Ban Mai              | Nữ miền Bắc (dịu dàng, chuẩn phát thanh viên, rất truyền cảm)                                    |
| `thanh-phuong-viettel` | Thanh Phương Viettel | Nữ miền Bắc (rõ ràng, lưu loát, dứt khoát, chuẩn phong cách tổng đài và trợ lý ảo chuyên nghiệp) |
| `mai-phuong`           | Mai Phương           | Nữ miền Bắc (nhẹ nhàng, ấm áp, thích hợp đọc sách nói và tin tức dài)                            |
| `phuong-trang`         | Phương Trang         | Nữ miền Bắc (trầm ấm, truyền cảm, phong cách thuyết minh)                                        |
| `duy-onyx-moi`         | Duy Onyx (mới)       | Nam miền Bắc (trầm ấm, hiện đại, ngữ điệu tự nhiên, rất hợp làm giọng trợ lý nam)                |
| `duy-oryx`             | Duy Oryx             | Nam miền Bắc (trầm, đĩnh đạc, chững chạc)                                                        |
| `minh-khang`           | Minh Khang           | Nam miền Bắc (trẻ trung, năng động, cuốn hút, phong cách kênh Kiến Giải Mã)                      |
| `minh-quang`           | Minh Quang           | Nam miền Bắc (chững chạc, phát âm chuẩn, phong cách bản tin thời sự)                             |
| `manh-dung`            | Mạnh Dũng            | Nam miền Bắc (hào sảng, khỏe khoắn, dứt khoát, phong cách phóng sự - ký sự)                      |
| `chieu-thanh`          | Chiếu Thành          | Nam miền Nam (chất giọng trầm ấm, phong cách đọc truyện kiếm hiệp và dã sử)                      |
| `thien-tam`            | Thiện Tâm            | Nam miền Nam (từ tốn, sâu lắng, điềm tĩnh, phong cách audio tâm sự và triết lý)                  |
| `ngoc-ngan`            | Ngọc Ngạn            | Nam miền Bắc (trầm, hóm hỉnh, phong cách MC kể chuyện Paris By Night đặc trưng)                  |
| `tran-thanh`           | Trấn Thành           | Nam miền Nam (hoạt ngôn, biểu cảm đa dạng, sinh động và vui vẻ)                                  |
| `viet-thao`            | Việt Thảo            | Nam miền Nam (hóm hỉnh, hoạt náo, gần gũi, phong cách MC sân khấu)                               |
| `tai-an`               | Tài An               | Nam miền Bắc (rành mạch, phong cách thuyết minh lịch sử CD Media)                                |
| `lac-phi`              | Lạc Phi              | Nữ miền Bắc (truyền cảm, phong cách thuyết minh và review phim)                                  |
| `my-tam`               | Mỹ Tâm               | Nữ miền Trung / Nam (chất giọng ấm áp đặc trưng của ca sĩ Mỹ Tâm)                                |
| `my-tam-real`          | Mỹ Tâm Real          | Nữ miền Trung / Nam (chất giọng đặc trưng của ca sĩ Mỹ Tâm, tự nhiên và chân thực)               |
| `adam`                 | adam                 | Nam quốc tế (âm sắc ElevenLabs Adam đọc tiếng Việt chuẩn xác)                                    |

#### Bảng mã giọng đọc engine ZeroTTS (Neural 48 kHz)

| Mã giọng (`id`) | Tên hiển thị | Vùng miền / Đặc trưng phong cách                                                          |
| :-------------- | :----------- | :---------------------------------------------------------------------------------------- |
| `maichi`        | Mai Chi      | Nữ miền Bắc (nhẹ nhàng, thân thiện, tự nhiên như trò chuyện ngoài đời thực)               |
| `baotrang`      | Bảo Trang    | Nữ miền Bắc (phong thái trưởng thành, đĩnh đạc, rõ ràng, trung tính, rất hợp đọc tin tức) |
| `giahuy`        | Gia Huy      | Nam miền Bắc (giọng trẻ, trầm ấm, tâm tình, thích hợp kể chuyện và đối thoại thân mật)    |
| `hamy`          | Hà My        | Nữ miền Bắc (giọng trẻ, tông cao trong sáng, biểu cảm sinh động, phong cách năng động)    |
| `huuduc`        | Hữu Đức      | Nam miền Bắc (chất giọng lớn tuổi, điềm đạm, trầm ấm, phong cách kể chuyện truyền thống)  |
| `kimoanh`       | Kim Oanh     | Nữ miền Bắc (độ tuổi trung niên, ấm áp, giàu cảm xúc, phong cách đọc truyện và tâm tình)  |
| `quangminh`     | Quang Minh   | Nam miền Bắc (giọng trẻ, dứt khoát, sáng rõ, chuẩn phong cách phát thanh viên tin tức)    |
| `tiendat`       | Tiến Đạt     | Nam miền Bắc (giọng trẻ, sôi nổi, năng lượng cao, phong cách bình luận viên)              |

Mỗi giọng thêm vào đều được tải về và giữ trong bộ nhớ, nên bạn chỉ nên chọn những giọng thực sự dùng đến. Với các thiết bị cấu hình yếu, chỉ nên chọn 1 giọng đọc cùng engine `nghitts` để đạt hiệu năng mượt mà và tối ưu tài nguyên nhất.

---

## Triển khai bằng Docker

Dịch vụ này cũng có thể chạy độc lập bên ngoài Home Assistant.

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

Khi muốn cập nhật ảnh mới hoặc thay đổi biến môi trường, hãy tải ảnh mới nhất, xóa container cũ rồi khởi chạy lại. Hai volume có tên (`wyoming-vietnamese-cache` và `wyoming-vietnamese-models`) vẫn được giữ nguyên nên mô hình không cần phải tải lại:

```bash
docker pull ghcr.io/luuquangvu/wyoming-vietnamese:latest
docker rm -f wyoming-vietnamese
```

### Tự biên dịch ảnh Docker từ mã nguồn

Dành cho các lập trình viên hoặc người dùng muốn tùy biến sâu mã nguồn:

```bash
git clone https://github.com/luuquangvu/wyoming-vietnamese.git
cd wyoming-vietnamese
docker compose up --build -d
```

---

## Xử lý sự cố thường gặp (Troubleshooting)

### 1. Home Assistant báo lỗi không kết nối được tới Wyoming Protocol ("Failed to connect")

- **Kiểm tra trạng thái App**: Đảm bảo App Wyoming Vietnamese đang trong trạng thái khởi chạy thành công và cổng `10300` đang mở.
- **Xem nhật ký (Log)**: Mở tab **Log** trong trang cấu hình App để kiểm tra xem dịch vụ đã in dòng thông báo sẵn sàng ở cổng `10300` chưa (`Wyoming STT/TTS service is ready at tcp://0.0.0.0:10300`).
- **Kiểm tra tường lửa (Firewall)**: Đảm bảo cổng `10300` trên máy chủ Home Assistant không bị chặn bởi tường lửa hệ điều hành hoặc cấu hình mạng.
- **Kiểm tra địa chỉ Host**: Nhập chính xác địa chỉ IP trong mạng LAN của máy chủ Home Assistant (ví dụ `192.168.1.100` hoặc `homeassistant.local`), tránh sử dụng `localhost` nếu Home Assistant và dịch vụ nằm trên hai môi trường tách biệt.

### 2. App khởi động chậm hoặc bị dừng ở lần chạy đầu tiên

- **Kiểm tra kết nối Internet**: Ở lần chạy đầu tiên, App bắt buộc phải có Internet để tải mô hình nhận diện giọng nói (STT Zipformer) và các giọng đọc TTS được chọn. Quá trình tải có thể mất từ 1 đến 3 phút tùy tốc độ mạng.
- **Theo dõi tiến trình tải**: Mở tab **Log** theo thời gian thực để theo dõi tiến độ tải file và xác thực mã băm SHA-256.
- **Cấu hình phần cứng hạn chế**: Nếu thiết bị có dung lượng RAM thấp (dưới 2 GB), hãy chọn `tts_engine: nghitts` và chỉ cấu hình từ 1 đến 2 giọng đọc cần thiết nhất để tối ưu hóa bộ nhớ.

### 3. Đã đổi giọng trong `tts_voice` nhưng Home Assistant không hiển thị giọng mới

- Các tùy chọn cấu hình chỉ có hiệu lực khi App khởi động lại. Sau khi lưu cấu hình và khởi động lại App, bạn hãy vào Home Assistant > **Cài đặt (Settings)** > **Thiết bị & Dịch vụ (Devices & Services)** > tìm tích hợp **Wyoming Protocol** > bấm vào biểu tượng dấu 3 chấm góc phải và chọn **Tải lại (Reload)** để Home Assistant đồng bộ danh sách giọng mới.

### 4. Giọng đọc bị giật cục hoặc phản hồi chậm trên Raspberry Pi

- Hãy chuyển sang sử dụng engine `nghitts` (`tts_engine: nghitts`). Engine này sử dụng mô hình VITS siêu nhẹ, được tối ưu hóa riêng cho các kiến trúc ARM như Raspberry Pi 4/5. Engine `zerotts` sử dụng mô hình ngôn ngữ giọng nói AI lớn hơn nhiều, chỉ phù hợp khi chạy trên các máy chủ có CPU x86 tương đối mạnh.

---

## Lời cảm ơn

Dự án được xây dựng và hoàn thiện dựa trên các công trình mã nguồn mở xuất sắc:

- [nghimestudio/nghitts](https://github.com/nghimestudio/nghitts): Cung cấp các mô hình giọng đọc tiếng Việt (TTS) chất lượng cao cho engine `nghitts`.
- [zeroweight-ai/ZeroTTS](https://github.com/zeroweight-ai/ZeroTTS): Cung cấp mô hình ngôn ngữ giọng nói ZeroTTS và runtime C++ GGML cho engine `zerotts`.
- [hynt](https://huggingface.co/hynt): Cung cấp mô hình nhận diện giọng nói tiếng Việt `Zipformer-30M-RNNT-6000h` (STT).
- [k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx): Thư viện suy luận offline tối ưu cao cho cả STT và TTS.
- [Wyoming Protocol](https://github.com/OHF-Voice/wyoming): Chuẩn giao thức mở cho trợ lý giọng nói trong hệ sinh thái Home Assistant.
