# Google Gemini cho Home Assistant

[![Home Assistant Add-on](https://img.shields.io/badge/Home%20Assistant-Add--on-blue?style=for-the-badge&logo=home-assistant)](https://github.com/luuquangvu/ha-addons)

**[ [🇺🇸 English](README.md) | 🇻🇳 Tiếng Việt ]**

Tích hợp trực tiếp trí tuệ nhân tạo Gemini của Google vào hệ sinh thái Home Assistant. Add-on này cung cấp một cổng API tương thích với OpenAI, cho phép Home Assistant Assist, các bot hội thoại và kịch bản tự động hóa tận dụng sức mạnh của AI tạo sinh (Generative AI) tiên tiến mà không cần đăng ký Google Cloud API key.

> [!NOTE]
> Add-on này sử dụng một bản fork chuyên biệt của [Gemini-FastAPI](https://github.com/luuquangvu/Gemini-FastAPI) được tối ưu hóa để tích hợp mượt mà và cập nhật nhanh chóng cho Home Assistant.

---

## Tính năng Kỹ thuật

- **API Tương thích OpenAI**: Tích hợp dễ dàng với bất kỳ thành phần nào của Home Assistant hoặc ứng dụng bên thứ ba hỗ trợ tiêu chuẩn API OpenAI.
- **Hỗ trợ Mô hình**: Truy cập các mô hình Gemini Pro, Gemini Flash Thinking và Gemini Flash.
- **Xác thực qua Cookie**: Truy cập Gemini thông qua session cookie trình duyệt, loại bỏ các bước cấu hình phức tạp trên Google Cloud Project.
- **Ngữ cảnh Hội thoại**: Hỗ trợ hội thoại đa lượt với khả năng ghi nhớ, giúp việc điều khiển nhà thông minh trở nên tự nhiên hơn.
- **Tìm kiếm Google (Grounding)**: Tận dụng thông tin thời gian thực từ web để cung cấp câu trả lời chính xác.
- **Xử lý Đa phương thức**: Hỗ trợ trực tiếp việc xử lý văn bản, hình ảnh và tệp tin đính kèm trong các kịch bản tự động hóa.
- **Tối ưu cho Home Assistant**: Thiết kế để vận hành nội bộ với cấu hình đơn giản qua YAML hoặc biến môi trường.

---

## Lưu ý về Bảo mật và Quyền riêng tư

- **Phương thức Xác thực**: Add-on này sử dụng cookie trình duyệt để xác thực với dịch vụ Google Gemini. Việc này có thể vi phạm Điều khoản dịch vụ của Google, dẫn đến rủi ro tài khoản bị hạn chế.
- **Khuyến nghị**: Chúng tôi **đặc biệt khuyến nghị** bạn nên sử dụng một **tài khoản Google phụ tách biệt** để đảm bảo an toàn cho dữ liệu chính của mình.

---

## Hướng dẫn Cài đặt và Cấu hình

### Bước 1: Cài đặt Add-on

1. Thêm kho lưu trữ [**luuquangvu/ha-addons**](https://github.com/luuquangvu/ha-addons) vào Cửa hàng Add-on của Home Assistant.
2. Tìm và cài đặt **Gemini FastAPI**.
3. **Khởi động Add-on một lần.** Dịch vụ sẽ tự động tạo các tệp cấu hình mặc định và sau đó dừng lại.

### Bước 2: Lấy Cookie Xác thực

1. Mở cửa sổ trình duyệt **Ẩn danh (Private/Incognito)**.
2. Đăng nhập vào [https://gemini.google.com](https://gemini.google.com) bằng tài khoản Google phụ.
3. Mở **Công cụ nhà phát triển** (F12 hoặc Chuột phải > Kiểm tra).
4. Chuyển đến tab **Application** (Chrome/Edge) hoặc **Storage** (Firefox).
5. Trong mục **Cookies**, chọn `https://gemini.google.com` và lấy các giá trị:
   - `__Secure-1PSID`
   - `__Secure-1PSIDTS`
6. **Đóng cửa sổ ẩn danh ngay lập tức** sau khi sao chép để tránh xung đột phiên đăng nhập.

### Bước 3: Cấu hình Dịch vụ

1. Sử dụng trình soạn thảo tệp (ví dụ: Studio Code Server) truy cập vào `/homeassistant/gemini-fastapi/config/`.
2. Chỉnh sửa tệp `config.yaml` để điền cookie đã lấy:

   ```yaml
   gemini:
     clients:
       - id: "ha-gemini"
         secure_1psid: "DÁN_SECURE_1PSID_TẠI_ĐÂY"
         secure_1psidts: "DÁN_SECURE_1PSIDTS_TẠI_ĐÂY"
   ```

3. **(Khuyến nghị)** Bảo mật endpoint API bằng cách định nghĩa một mã token bí mật:

   ```yaml
   server:
     api_key: "ma-token-bi-mat-cua-ban"
   ```

### Bước 4: Khởi chạy

1. Quay lại trang Add-on Gemini FastAPI và nhấn **Start**.
2. Kiểm tra tab **Log** để xác nhận dịch vụ đã khởi tạo thành công.

---

## Tích hợp với Home Assistant

Để sử dụng Gemini như một trợ lý hội thoại, chúng tôi khuyên dùng tích hợp [**Local OpenAI LLM**](https://github.com/luuquangvu/hass_local_openai_llm).

1. **Cài đặt qua HACS**:
   [![Mở HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=luuquangvu&repository=hass_local_openai_llm&category=integration)
2. **Thêm Tích hợp**: Truy cập **Cấu hình > Thiết bị & Dịch vụ** và tìm "Local OpenAI LLM".
3. **Cấu hình Kết nối**:
   - **Base URL**: `http://IP_CỦA_HA:8000/v1` (hoặc `http://127.0.0.1:8000/v1` nếu chạy trên cùng host)
   - **API Key**: Mã `api_key` bạn đã định nghĩa trong `config.yaml`.

---

## Triển khai bằng Docker

### Docker Compose

```yaml
services:
  gemini-fastapi:
    image: ghcr.io/luuquangvu/gemini-fastapi:latest
    container_name: gemini-fastapi
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./cache:/app/cache
    environment:
      - "TZ=Asia/Ho_Chi_Minh"
      - "CONFIG_SERVER__API_KEY=your-api-key"
      - "CONFIG_GEMINI__CLIENTS__0__ID=main-client"
      - "CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID=your-1psid"
      - "CONFIG_GEMINI__CLIENTS__0__SECURE_1PSIDTS=your-1psidts"
      - "GEMINI_COOKIE_PATH=/app/cache"
```

### Docker CLI

```bash
docker run -d --name gemini-fastapi \
  -p 8000:8000 \
  -v ./data:/app/data \
  -v ./cache:/app/cache \
  -e "CONFIG_SERVER__API_KEY=your-api-key" \
  -e "CONFIG_GEMINI__CLIENTS__0__ID=main-client" \
  -e "CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID=your-1psid" \
  -e "CONFIG_GEMINI__CLIENTS__0__SECURE_1PSIDTS=your-1psidts" \
  -e "GEMINI_COOKIE_PATH=/app/cache" \
  ghcr.io/luuquangvu/gemini-fastapi:latest
```

---

## Xử lý Sự cố

- **Lỗi Xác thực**: Nếu log báo lỗi khởi tạo, cookie phiên làm việc của bạn có thể đã hết hạn. Vui lòng thực hiện lại quy trình lấy cookie.
- **Lỗi Kết nối**: Đảm bảo cổng `8000` có thể truy cập được và `api_key` khớp chính xác với cấu hình trong Home Assistant.
- **Độ ổn định Phiên**: Nếu cookie hết hạn thường xuyên, hãy thử sử dụng trình duyệt khác (ví dụ: Firefox) để lấy cookie.

---

## Lời cảm ơn

- Xây dựng dựa trên thư viện [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API).
