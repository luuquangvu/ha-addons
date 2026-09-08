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
- **20 giọng tiếng Việt**: Chọn một hoặc nhiều giọng; giọng đầu tiên trong cấu hình là giọng mặc định trong Assist.
- **Lưu mô hình cố định**: Mô hình chỉ tải một lần vào phân vùng `/data` của App, nên các lần khởi động sau nhanh hơn.
- **Chế độ ngoại tuyến**: Sau khi tải đủ mô hình, dịch vụ có thể chạy hoàn toàn không cần Internet.
- **Ngắt nghỉ tự nhiên theo chuẩn ngữ pháp**: Tự động căn chỉnh khoảng nghỉ giữa đoạn văn, câu và vế câu (dấu phẩy), giúp câu văn mạch lạc, không bị dồn chữ.

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

| Tùy chọn    | Mặc định                                                                    | Mô tả                                                                                                 |
| ----------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `tts_voice` | `ngoc-huyen-moi, duy-onyx-moi, thanh-phuong-viettel, ngoc-ngan, mai-phuong` | Một hoặc nhiều mã giọng, ngăn cách bằng dấu phẩy và/hoặc khoảng trắng. Mã đầu tiên là giọng mặc định. |
| `log_level` | `info`                                                                      | Đặt `debug` khi cần xem nhật ký chi tiết để chẩn đoán sự cố.                                          |

### Các giọng có sẵn

| Mã giọng (`id`)        | Tên hiển thị         | Vùng miền / Đặc trưng                                                  | Mặc định |
| :--------------------- | :------------------- | :--------------------------------------------------------------------- | :------: |
| `ngoc-huyen-moi`       | Ngọc Huyền (mới)     | Nữ miền Bắc (tự nhiên, trong trẻo, phong cách đọc truyện và review)    |  **Có**  |
| `ban-mai`              | Ban Mai              | Nữ miền Bắc (dịu dàng, truyền cảm, phong cách phát thanh viên)         |          |
| `thanh-phuong-viettel` | Thanh Phương Viettel | Nữ miền Bắc (rõ ràng, lưu loát, chuẩn phong cách trợ lý và tổng đài)   |          |
| `mai-phuong`           | Mai Phương           | Nữ miền Bắc (nhẹ nhàng, ấm áp, phong cách đọc sách nói)                |          |
| `phuong-trang`         | Phương Trang         | Nữ miền Bắc (trầm ấm, truyền cảm, phong cách thuyết minh)              |          |
| `duy-onyx-moi`         | Duy Onyx (mới)       | Nam miền Bắc (trầm ấm, tự nhiên, phong cách trợ lý nam)                |          |
| `duy-oryx`             | Duy Oryx             | Nam miền Bắc (trầm, đĩnh đạc)                                          |          |
| `minh-khang`           | Minh Khang           | Nam miền Bắc (trẻ trung, cuốn hút, phong cách kênh Kiến Giải Mã)       |          |
| `minh-quang`           | Minh Quang           | Nam miền Bắc (chững chạc, rõ ràng, phong cách đọc tin tức)             |          |
| `manh-dung`            | Mạnh Dũng            | Nam miền Bắc (hào sảng, dứt khoát, phong cách ký sự và tài liệu)       |          |
| `chieu-thanh`          | Chiếu Thành          | Nam miền Nam (trầm ấm, phong cách kể chuyện kiếm hiệp và dã sử)        |          |
| `thien-tam`            | Thiện Tâm            | Nam miền Nam (từ tốn, sâu lắng, phong cách tâm sự và audio Phật giáo)  |          |
| `ngoc-ngan`            | Ngọc Ngạn            | Nam miền Bắc (trầm, hóm hỉnh, phong cách MC dẫn chuyện Paris By Night) |          |
| `tran-thanh`           | Trấn Thành           | Nam miền Nam (hoạt ngôn, biểu cảm, phong cách nghệ sĩ hài hước)        |          |
| `viet-thao`            | Việt Thảo            | Nam miền Nam (hóm hỉnh, gần gũi, phong cách MC sân khấu)               |          |
| `tai-an`               | Tài An               | Nam miền Bắc (rành mạch, phong cách thuyết minh lịch sử CD Media)      |          |
| `lac-phi`              | Lạc Phi              | Nữ miền Bắc (truyền cảm, phong cách thuyết minh và review phim)        |          |
| `my-tam`               | Mỹ Tâm               | Nữ miền Nam / Miền Trung (giọng ca sĩ Mỹ Tâm, âm vị chuẩn toàn quốc)   |          |
| `my-tam-real`          | Mỹ Tâm Real          | Nữ miền Nam (giọng ca sĩ Mỹ Tâm, ngữ điệu miền Nam chân thực)          |          |
| `adam`                 | adam                 | Nam quốc tế (chất giọng ElevenLabs Adam đọc tiếng Việt)                |          |

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
      WYOMING_PORT: 10300
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
docker run -d --name wyoming-vietnamese \
  --restart unless-stopped \
  -p 10300:10300 \
  -e "TTS_VOICE=ngoc-huyen-moi, duy-onyx-moi, thanh-phuong-viettel, ngoc-ngan, mai-phuong" \
  -e "LOG_LEVEL=info" \
  -v wyoming-vietnamese-cache:/app/.cache \
  -v wyoming-vietnamese-models:/app/models \
  ghcr.io/luuquangvu/wyoming-vietnamese:latest
```

---

## Xử lý Sự cố

- **Không thêm được Wyoming trong Home Assistant**: Kiểm tra App đang chạy và cổng `10300` có thể truy cập được. Xem tab **Log** để tìm lỗi khởi động.
- **App khởi động lâu ở lần đầu**: Mô hình STT và từng giọng được tải ở lần khởi động đầu tiên. Hãy giữ kết nối Internet cho tới khi nhật ký báo dịch vụ đã sẵn sàng.
- **Đổi giọng nhưng Home Assistant vẫn đọc giọng cũ**: Đối chiếu mã giọng với bảng ở trên, khởi động lại App, rồi mở lại trang Trợ lý giọng nói hoặc chọn Tải lại (Reload) tích hợp Wyoming Protocol trong Home Assistant.

---

## Lời cảm ơn

- [nghimestudio/nghitts](https://github.com/nghimestudio/nghitts) cung cấp các mô hình giọng đọc tiếng Việt.
- [hynt](https://huggingface.co/hynt) cung cấp mô hình nhận diện STT `Zipformer-30M-RNNT-6000h`.
- [k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) cung cấp bộ máy suy luận STT và TTS.
- [Wyoming Protocol](https://github.com/OHF-Voice/wyoming) giúp kết nối dịch vụ với hệ sinh thái Home Assistant Voice.
