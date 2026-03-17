# Tích hợp Google Gemini cho Home Assistant - AI Miễn phí & Không giới hạn

**[ [🇺🇸 English](README.md) | 🇻🇳 Tiếng Việt ]**

[![GitHub License](https://img.shields.io/github/license/luuquangvu/ha-addons?style=for-the-badge&labelColor=000000)](https://github.com/luuquangvu/ha-addons/blob/main/LICENSE)

Việc mang **Google Gemini vào Home Assistant** chưa bao giờ dễ dàng và mạnh mẽ đến thế. App (tên cũ là add-on) này giúp bạn tích hợp dịch vụ AI Gemini trực tiếp vào hệ thống nhà thông minh của mình. Bằng cách cung cấp một API tương thích với OpenAI, ứng dụng cho phép Home Assistant và các trợ lý ảo (Assist) tương tác với các mô hình Gemini mạnh mẽ hoàn toàn miễn phí mà không cần API key chính thức.

> App này sử dụng một bản fork từ dự án gốc ([luuquangvu/Gemini-FastAPI](https://github.com/luuquangvu/Gemini-FastAPI)) để cập nhật các tính năng mới nhanh hơn.

## Các tính năng nổi bật của Gemini cho Home Assistant

- **Hoàn toàn miễn phí & Không giới hạn**: Trải nghiệm các mô hình **Gemini Pro** và **Gemini Flash** mới nhất mà không mất phí duy trì hàng tháng.
- **Không cần Google API Key**: Hoạt động an toàn dựa trên cookie trình duyệt, không cần đăng ký thẻ tín dụng hay chờ xét duyệt API.
- **Tương thích hoàn toàn API OpenAI**: Kết nối mượt mà với bất kỳ tích hợp Home Assistant hoặc ứng dụng nào hỗ trợ chuẩn OpenAI.
- **Lưu trữ hội thoại thông minh**: Trợ lý ảo AI của bạn sẽ ghi nhớ các trao đổi trước đó, duy trì ngữ cảnh ngay cả khi khởi động lại.
- **Tích hợp Google Tìm kiếm**: Cung cấp các câu trả lời cập nhật thời gian thực từ internet cho nhà thông minh của bạn.
- **Hỗ trợ đa phương thức (Multi-modal)**: Khả năng nhận diện và xử lý hình ảnh, văn bản và tệp tin cho các kịch bản tự động hóa nâng cao.
- **Cấu hình tối ưu cho HA**: Dễ dàng tùy chỉnh qua YAML hoặc biến môi trường, thiết kế riêng cho hệ sinh thái Home Assistant.

---

## Lưu ý quan trọng: Trước khi bắt đầu

- **Rủi ro sử dụng**: Việc sử dụng cookie trình duyệt để truy cập Gemini có thể vi phạm Điều khoản dịch vụ của Google, dẫn đến rủi ro tài khoản bị hạn chế.
- **Khuyến nghị**: Để đảm bảo an toàn, bạn **nên sử dụng một tài khoản Google phụ** (không phải tài khoản chính) cho App này.

---

## Hướng dẫn Cài đặt & Cấu hình

### Bước 1: Cài đặt App

1. Đảm bảo bạn đã thêm [**Kho Apps cho Home Assistant**](https://github.com/luuquangvu/ha-addons) vào Cửa hàng Apps.
2. Tìm và cài đặt App **Gemini FastAPI**.
3. **Khởi động App một lần.** App sẽ tự động tạo các tệp cấu hình cần thiết rồi dừng lại.

### Bước 2: Lấy Cookie Google Gemini

1. Mở trình duyệt ở chế độ **Ẩn danh (Incognito/Private)**.
2. Truy cập [https://gemini.google.com](https://gemini.google.com) và đăng nhập bằng tài khoản Google phụ.
3. Mở Công cụ dành cho nhà phát triển (Developer Tools - phím `F12`).
4. Chuyển đến tab **Application** > **Storage**.
5. Trong mục **Cookies**, chọn `https://gemini.google.com` và sao chép giá trị của:
   - `__Secure-1PSID`
   - `__Secure-1PSIDTS`
6. Lưu lại các giá trị này.
7. **Đóng cửa sổ ẩn danh ngay sau khi sao chép** để tránh xung đột cookie hoặc hết hạn phiên làm việc sớm.

### Bước 3: Cấu hình App

1. Sử dụng trình chỉnh sửa tệp (như Studio Code Server), truy cập thư mục `/homeassistant/gemini-fastapi/config/`.
2. Mở tệp `config.yaml`.
3. Điền các giá trị cookie đã lấy ở Bước 2:

   ```yaml
   gemini:
     clients:
       - id: "client-a" # Đặt tên bất kỳ cho client
         secure_1psid: "DÁN_GIÁ_TRỊ_SECURE_1PSID_VÀO_ĐÂY"
         secure_1psidts: "DÁN_GIÁ_TRỊ_SECURE_1PSIDTS_VÀO_ĐÂY"
   ```

4. (Khuyến nghị) Bảo mật API endpoint bằng token bằng cách thêm `api_key` trong phần `server`:

   ```yaml
   server:
     api_key: "token-bi-mat-cua-ban"
   ```

5. Lưu tệp `config.yaml`.

### Bước 4: Khởi động lại & Xác minh

1. Quay lại trang App Gemini FastAPI.
2. Nhấn **Restart**.
3. Kiểm tra tab **Log** để đảm bảo không có lỗi khởi động.

> [!NOTE]
> App sử dụng cổng 8000. Bạn nên đặt `api_key` (như Bước 3) để bảo vệ dữ liệu, nhất là khi mở truy cập từ xa qua các dịch vụ như Nginx Proxy Manager.

### Xử lý sự cố & Cập nhật Cookie

Vì App dựa trên cookie trình duyệt, chúng có thể hết hạn (ví dụ: khi bạn đăng xuất Google hoặc phiên làm việc kết thúc).

- **Dấu hiệu**: App không phản hồi hoặc Log báo lỗi `Failed to initialize client ...`.
- **Cách sửa**: Lặp lại **Bước 2** và **Bước 3** để lấy cookie mới, cập nhật vào `config.yaml` và khởi động lại App.

> [!TIP]
> Nếu cookie thường xuyên hết hạn, hãy thử lấy cookie từ một trình duyệt khác.

### Kết nối Gemini với Trợ lý ảo Home Assistant (Assist)

Để sử dụng **Gemini cho Home Assistant** làm trợ lý ảo điều khiển bằng giọng nói (Assist), bạn cần một tích hợp hỗ trợ chuẩn OpenAI API.

#### Khuyên dùng: Local OpenAI LLM

Bạn nên sử dụng tích hợp [**Local OpenAI LLM**](https://github.com/luuquangvu/hass_local_openai_llm). Đây là bản fork được tối ưu hóa riêng cho App này.

1.  **Cài đặt qua HACS**:
    - **Tự động**: Nhấn nút bên dưới để mở nhanh trong HACS:

      [![Open HACS Repository](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=luuquangvu&repository=hass_local_openai_llm&category=integration)

    - **Thủ công**: Thêm `https://github.com/luuquangvu/hass_local_openai_llm` làm **Custom Repository** (Category: Integration) trong HACS.

    - Tải xuống và **Khởi động lại** Home Assistant.

2.  **Thêm tích hợp**: Vào **Settings > Devices & Services** > **Add Integration** > Tìm **Local OpenAI LLM**.

3.  **Cấu hình**:
    - **Server URL**: `http://127.0.0.1:8000/v1`
    - **API Key**: Token bạn đã đặt trong `config.yaml`.

---

## Triển khai Docker độc lập (Standalone)

Dành cho người dùng chạy dịch vụ ngoài môi trường Home Assistant.

### Sử dụng Docker Compose

Tạo tệp `compose.yaml`:

```yaml
services:
  gemini-fastapi:
    container_name: gemini-fastapi
    image: ghcr.io/luuquangvu/gemini-fastapi:latest
    pull_policy: always
    restart: on-failure:3
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./cache:/app/cache
      # - ./config:/app/config # Bỏ dấu chú thích để sử dụng tệp cấu hình thay vì biến môi trường
      # - ./certs:/app/certs # Bỏ dấu chú thích để bật HTTPS
    environment:
      - "TZ=Asia/Ho_Chi_Minh"
      - "CONFIG_SERVER__HOST=0.0.0.0"
      - "CONFIG_SERVER__PORT=8000"
      - "CONFIG_SERVER__API_KEY=your-api-key-here"
      - "CONFIG_GEMINI__CLIENTS__0__ID=client-a"
      - "CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID=your-secure-1psid"
      - "CONFIG_GEMINI__CLIENTS__0__SECURE_1PSIDTS=your-secure-1psidts"
      # - "CONFIG_GEMINI__CLIENTS__0__PROXY=socks5://127.0.0.1:1080" # Bỏ dấu chú thích để bật proxy cho từng client
      - "GEMINI_COOKIE_PATH=/app/cache"
```

Chạy lệnh: `docker compose up -d`

> [!IMPORTANT]
>
> - Mount `/app/data` để lưu lịch sử hội thoại.
> - Mount `/app/cache` để lưu cookie đã làm mới, tránh việc phải đăng nhập lại thường xuyên.

---

## Tùy chỉnh Mô hình (Custom Models)

Bạn có thể định nghĩa thêm các mô hình trong `config.yaml` hoặc qua biến môi trường.

### Cấu hình YAML

```yaml
gemini:
  model_strategy: "append" # "append" (mặc định + tùy chỉnh) hoặc "overwrite" (chỉ dùng tùy chỉnh)
  models:
    - model_name: "gemini-3.0-pro"
      model_header:
        x-goog-ext-525001261-jspb: '[1,null,null,null,"9d8ca3786ebdfbea",null,null,0,[4],null,null,1]'
```

---

## Lời cảm ơn (Acknowledgments)

- **Gemini API Client**: [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API)
