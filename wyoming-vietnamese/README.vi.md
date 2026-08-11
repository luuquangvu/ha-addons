# Wyoming Vietnamese cho Home Assistant

[![Home Assistant App](https://img.shields.io/badge/Home%20Assistant-Add--on-blue?style=for-the-badge&logo=home-assistant)](https://github.com/luuquangvu/ha-addons)

**[🇺🇸 English](README.md) | 🇻🇳 Tiếng Việt**

Giúp Assist của Home Assistant nghe và trả lời bằng tiếng Việt tự nhiên, ngay trong mạng nhà bạn. App này gói cả dịch vụ **chuyển giọng nói thành văn bản (STT)** và **chuyển văn bản thành giọng nói (TTS)** vào một dịch vụ Wyoming Protocol duy nhất, nên Home Assistant chỉ cần kết nối tới một địa chỉ và một cổng.

> [!NOTE]
> App này đóng gói ảnh dịch vụ [Wyoming Vietnamese](https://github.com/luuquangvu/wyoming-vietnamese) cho Home Assistant, với mô hình (model) được lưu trong phân vùng `/data` cố định của App.

---

## Tính năng Kỹ thuật

- **Gộp STT và TTS**: Cả hai dịch vụ dùng chung cổng Wyoming `10300`.
- **Chạy nội bộ hoàn toàn**: Không cần tài khoản đám mây hay khóa API (API key). Âm thanh và văn bản không phải gửi tới dịch vụ bên ngoài trong quá trình sử dụng.
- **19 giọng tiếng Việt**: Chọn một hoặc nhiều giọng; giọng đầu tiên trong cấu hình là giọng mặc định trong Assist.
- **Lưu mô hình cố định**: Mô hình chỉ tải một lần vào phân vùng `/data` của App, nên các lần khởi động sau nhanh hơn.
- **Chế độ ngoại tuyến**: Sau khi tải đủ mô hình, dịch vụ có thể chạy hoàn toàn không cần Internet.
- **Nhịp đọc tự nhiên**: Khoảng nghỉ giữa câu, giữa mệnh đề và độ ngẫu nhiên đều có thể tùy chỉnh để tránh giọng đọc máy móc.

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
> Sau khi thay đổi tùy chọn, hãy **khởi động lại (Restart)** App. Các tùy chọn chỉ được đọc khi tiến trình khởi động.

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

| Tùy chọn                     | Mặc định                    | Mô tả                                                                                                 |
| ---------------------------- | --------------------------- | ----------------------------------------------------------------------------------------------------- |
| `tts_voice`                  | `ngoc-huyen-moi, ngoc-ngan` | Một hoặc nhiều mã giọng, ngăn cách bằng dấu phẩy và/hoặc khoảng trắng. Mã đầu tiên là giọng mặc định. |
| `cpu_threads`                | `0`                         | Số luồng CPU dùng cho suy luận. Để `0` để tự động dùng số luồng phù hợp.                              |
| `offline`                    | `false`                     | Chỉ đặt `true` sau khi đã tải đủ mô hình. Khi thiếu mô hình, App sẽ báo lỗi thay vì kết nối Internet. |
| `tts_sentence_silence_ms`    | `400`                       | Khoảng nghỉ giữa các câu, tính bằng mili giây. Tăng giá trị nếu giọng đọc hơi nhanh.                  |
| `tts_clause_silence_ms`      | `180`                       | Khoảng nghỉ sau dấu phẩy và các dấu câu trong mệnh đề, tính bằng mili giây.                           |
| `tts_silence_jitter_percent` | `25`                        | Mức thay đổi ngẫu nhiên +/- cho mỗi khoảng nghỉ, giúp câu đọc tự nhiên hơn.                           |
| `log_level`                  | `info`                      | Đặt `debug` khi cần xem nhật ký chi tiết để chẩn đoán sự cố.                                          |

### Các giọng có sẵn

| Mã                     | Tên hiển thị         |
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

Mỗi giọng thêm vào đều được tải về và giữ trong bộ nhớ, nên bạn chỉ nên chọn những giọng thực sự dùng đến.

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

## Xử lý Sự cố

- **Không thêm được Wyoming trong Home Assistant**: Kiểm tra App đang chạy và cổng `10300` có thể truy cập được. Xem tab **Log** để tìm lỗi khởi động.
- **App khởi động lâu ở lần đầu**: Mô hình STT và từng giọng được tải ở lần khởi động đầu tiên. Hãy giữ kết nối Internet cho tới khi nhật ký báo dịch vụ đã sẵn sàng.
- **Khởi động lỗi khi bật `offline`**: Đặt `offline` về `false`, khởi động lại và chờ tải xong trước khi bật lại.
- **Đổi giọng nhưng Home Assistant vẫn đọc giọng cũ**: Đối chiếu mã giọng với bảng ở trên, khởi động lại App, rồi mở lại trang Trợ lý giọng nói.
- **Giọng đọc quá nhanh**: Tăng `tts_sentence_silence_ms` và `tts_clause_silence_ms`.

---

## Lời cảm ơn

- [nghimestudio/nghitts](https://github.com/nghimestudio/nghitts) cung cấp các mô hình giọng đọc tiếng Việt.
- [hynt](https://huggingface.co/hynt) cung cấp mô hình nhận diện `Zipformer-30M-RNNT-6000h`.
- [k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) cung cấp bộ máy suy luận STT và TTS.
- [Wyoming Protocol](https://github.com/OHF-Voice/wyoming) giúp kết nối dịch vụ với hệ sinh thái Home Assistant Voice.
