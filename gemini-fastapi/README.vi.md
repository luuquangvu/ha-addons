# Google Gemini cho Home Assistant

[![Home Assistant App](https://img.shields.io/badge/Home%20Assistant-Add--on-blue?style=for-the-badge&logo=home-assistant)](https://github.com/luuquangvu/ha-addons)

**[🇺🇸 English](README.md) | 🇻🇳 Tiếng Việt**

Tích hợp trực tiếp trí tuệ nhân tạo Gemini của Google vào hệ sinh thái Home Assistant. App này cung cấp một cổng API tương thích với OpenAI, cho phép Home Assistant Assist, các bot hội thoại và kịch bản tự động hóa tận dụng sức mạnh của AI tạo sinh (Generative AI) tiên tiến mà không cần đăng ký Google Cloud API key.

> [!NOTE]
> App này sử dụng một bản fork chuyên biệt của [Gemini-FastAPI](https://github.com/luuquangvu/Gemini-FastAPI) được tối ưu hóa để tích hợp mượt mà và cập nhật nhanh chóng cho Home Assistant.

---

## Tính năng Kỹ thuật

- **API Tương thích OpenAI**: Tích hợp dễ dàng với bất kỳ thành phần nào của Home Assistant hoặc ứng dụng bên thứ ba hỗ trợ tiêu chuẩn API OpenAI.
- **Hỗ trợ Mô hình**: Truy cập các mô hình Gemini Pro, Gemini Flash Thinking và Gemini Flash.
- **Xác thực qua Cookie**: Truy cập Gemini thông qua session cookie trình duyệt, loại bỏ các bước cấu hình phức tạp trên Google Cloud Project.
- **Ngữ cảnh Hội thoại**: Hỗ trợ hội thoại đa lượt với khả năng ghi nhớ, giúp việc điều khiển nhà thông minh trở nên tự nhiên hơn.
- **Tìm kiếm Google (Grounding)**: Tận dụng thông tin thời gian thực từ web để cung cấp câu trả lời chính xác.
- **Xử lý Đa phương thức**: Hỗ trợ trực tiếp việc xử lý văn bản, hình ảnh và tệp tin đính kèm trong các kịch bản tự động hóa.
- **Hỗ trợ nhiều tài khoản**: Thêm nhiều tài khoản Gemini để phân tán yêu cầu và giảm giới hạn tần suất.
- **Tối ưu cho Home Assistant**: Thiết kế để vận hành nội bộ với cấu hình đơn giản ngay trong tab **Cấu hình** của App.

---

## Lưu ý về Bảo mật và Quyền riêng tư

- **Phương thức Xác thực**: App này sử dụng cookie trình duyệt để xác thực với dịch vụ Google Gemini. Việc này có thể vi phạm Điều khoản dịch vụ của Google, dẫn đến rủi ro tài khoản bị hạn chế.
- **Khuyến nghị**: Chúng tôi **đặc biệt khuyến nghị** bạn nên sử dụng một **tài khoản Google phụ tách biệt** để đảm bảo an toàn cho dữ liệu chính của mình.

---

## Hướng dẫn Cài đặt và Cấu hình

### Bước 1: Cài đặt App

1. Thêm kho lưu trữ [**luuquangvu/ha-addons**](https://github.com/luuquangvu/ha-addons) vào Cửa hàng App của Home Assistant.
2. Tìm và cài đặt **Gemini FastAPI**.
3. Nhập cả hai cookie vào tab **Cấu hình** trước khi dùng App làm tác nhân hội thoại.

### Bước 2: Lấy Cookie Xác thực

1. Mở cửa sổ trình duyệt **Ẩn danh (Private/Incognito)**.
2. Đăng nhập vào [https://gemini.google.com](https://gemini.google.com) bằng tài khoản Google phụ.
3. Mở **Công cụ nhà phát triển** (F12 hoặc Chuột phải > Kiểm tra).
4. Chuyển đến tab **Application** (Chrome/Edge) hoặc **Storage** (Firefox).
5. Trong mục **Cookies**, chọn `https://gemini.google.com` và lấy các giá trị:
   - `__Secure-1PSID`
   - `__Secure-1PSIDTS`
6. **Đóng cửa sổ ẩn danh ngay lập tức** sau khi sao chép để tránh xung đột phiên đăng nhập.

### Bước 3: Cấu hình App

1. Mở App **Gemini FastAPI** và chuyển đến tab **Cấu hình**.
2. Trong mục **Tài khoản Gemini**, dán các giá trị vừa lấy vào tài khoản đầu tiên:
   - **Cookie Secure 1PSID** (bắt buộc): `__Secure-1PSID`
   - **Cookie Secure 1PSIDTS** (bắt buộc): `__Secure-1PSIDTS`
3. **(Tùy chọn)** Nếu dùng nhiều tài khoản Google, nhấn **Add** trong mục **Tài khoản Gemini** và nhập cookie cho tài khoản tiếp theo.
4. **(Khuyến nghị)** Bảo mật endpoint API bằng cách nhập **API key**.
5. Giữ các tùy chọn còn lại ở giá trị mặc định trừ khi bạn cần xử lý sự cố.
6. Nhấn **Lưu**.

> [!NOTE]
> Mỗi tài khoản cần **cả hai** cookie. Nếu chỉ điền một cookie, App sẽ dừng và báo lỗi rõ ràng. Nếu không cấu hình tài khoản nào, App sẽ chạy ở **chế độ khách**: có thể trả lời câu hỏi văn bản nhưng không có lịch sử hội thoại, không tải tệp lên và không chọn được mô hình.

> [!IMPORTANT]
> Cấu hình chỉ được quản lý trong tab **Cấu hình**. App sử dụng tệp `config/config.yaml` mặc định của upstream đi kèm trong image và không còn tạo, sao chép hay gộp tệp cấu hình trong `/homeassistant/gemini-fastapi/config`. Chỉ các tùy chọn bên dưới là có thể thay đổi; các cài đặt khác của upstream dùng giá trị mặc định. Ở lần khởi động đầu tiên sau khi cập nhật, App sẽ xóa thư mục cấu hình cũ `/homeassistant/gemini-fastapi/config` và chuyển dữ liệu hội thoại cũ `/homeassistant/gemini-fastapi/data` vào vùng lưu trữ `/data` riêng. Nếu chưa có tài khoản, App sẽ khởi động ở chế độ khách: hãy nhập cookie và API key trong tab **Cấu hình** rồi khởi động lại. `/homeassistant` vẫn được gắn cho lần di chuyển này và sẽ được bỏ ở một bản phát hành sau. Nếu thư mục không khả dụng, App vẫn khởi động và thử lại ở lần sau.

### Bước 4: Khởi chạy

1. Quay lại trang App Gemini FastAPI và nhấn **Start**.
2. Kiểm tra tab **Log** để xác nhận dịch vụ đã khởi tạo thành công.

### Các tùy chọn cấu hình

| Tùy chọn    | Mặc định            | Mô tả                                                                                                                                     |
| ----------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `api_key`   | trống               | Token tùy chọn mà ứng dụng dùng API phải gửi kèm. Để trống nếu không muốn xác thực.                                                       |
| `log_level` | `debug`             | Mức ghi log của App: `debug`, `info`, `warning`, `error` hoặc `critical`.                                                                 |
| `clients`   | một tài khoản trống | Danh sách tài khoản Gemini. Mỗi mục cần cả hai cookie và có thể có ID client, proxy. Nếu không có tài khoản nào, App chạy ở chế độ khách. |

#### Các trường của tài khoản Gemini

| Trường           | Mô tả                                                                                                         |
| ---------------- | ------------------------------------------------------------------------------------------------------------- |
| `id`             | Tùy chọn. Để trống để tạo ID ổn định từ cookie tài khoản. Đặt rõ nếu muốn tên dễ đọc hoặc cần ghim tài khoản. |
| `secure_1psid`   | **Bắt buộc** cùng với `secure_1psidts`. Cookie `__Secure-1PSID` lấy từ `gemini.google.com`.                   |
| `secure_1psidts` | **Bắt buộc** cùng với `secure_1psid`. Cookie `__Secure-1PSIDTS` lấy từ `gemini.google.com`.                   |
| `proxy`          | Proxy tùy chọn cho tài khoản này, ví dụ `socks5://127.0.0.1:1080`. Để trống để kết nối trực tiếp.             |

### Nhiều tài khoản Gemini

Mỗi mục trong **Tài khoản Gemini** được áp dụng thành một client Gemini riêng của upstream. Yêu cầu sẽ được phân tán trên tất cả tài khoản đã cấu hình, giúp giảm giới hạn tần suất của từng tài khoản.

- Mỗi tài khoản cần cả cookie `__Secure-1PSID` và `__Secure-1PSIDTS`. Mục chỉ có một trong hai cookie sẽ bị từ chối với lỗi rõ ràng.
- Nếu không cấu hình tài khoản nào, App chạy ở chế độ khách mà không dùng lại cookie đã lưu của tài khoản cũ. Phiên khách có thể trả lời câu hỏi văn bản nhưng không có lịch sử hội thoại, không tải tệp lên và không chọn được mô hình.
- Upstream khởi tạo các tài khoản lần lượt, nên mỗi tài khoản thêm có thể làm thời gian khởi động tăng tới 30 giây.
- ID client tự sinh được tạo từ cookie `__Secure-1PSID`, nên việc thêm, xóa hoặc đổi thứ tự tài khoản không làm thay đổi lịch sử hội thoại. Xoay cookie `1PSIDTS` không đổi ID; xoay cookie `1PSID` sẽ đổi ID, nên hãy đặt `id` rõ ràng nếu cần giữ lịch sử.
- Đặt `id` rõ ràng nếu muốn tên dễ đọc hoặc cần ghim tài khoản khi cookie thay đổi.
- Nếu đang nâng cấp và muốn tiếp tục hội thoại được lưu dưới ID client cũ (ví dụ `client-id-1`), hãy đặt rõ `id` đó cho tài khoản.
- Dùng **URL proxy** khác nhau cho từng tài khoản nếu các tài khoản cần kết nối qua proxy riêng.

---

## Tích hợp với Home Assistant

Để sử dụng Gemini như một trợ lý hội thoại, chúng tôi khuyên dùng tích hợp [**Local OpenAI LLM**](https://github.com/luuquangvu/hass_local_openai_llm).

1. **Cài đặt qua HACS**:
   [![Mở HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=luuquangvu&repository=hass_local_openai_llm&category=integration)
2. **Thêm Tích hợp**: Truy cập **Cấu hình > Thiết bị & Dịch vụ** và tìm "Local OpenAI LLM".
3. **Cấu hình Kết nối**:
   - **Base URL**: `http://IP_CỦA_HA:8000/v1` (hoặc `http://127.0.0.1:8000/v1` nếu chạy trên cùng host)
   - **API Key**: Mã `api_key` trong tab **Cấu hình** của App.

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

> [!TIP]
> Để dùng nhiều tài khoản Gemini, lặp lại các biến client với chỉ số liên tiếp: `CONFIG_GEMINI__CLIENTS__0__...`, `CONFIG_GEMINI__CLIENTS__1__...`, v.v.

---

## Xử lý Sự cố

- **Lỗi Xác thực**: Nếu log báo lỗi khởi tạo, cookie phiên làm việc của bạn có thể đã hết hạn. Vui lòng thực hiện lại quy trình lấy cookie. Cần cả cookie `__Secure-1PSID` và `__Secure-1PSIDTS`.
- **Chế độ khách**: Nếu không cấu hình tài khoản nào, App chạy ở chế độ khách và chỉ trả lời được câu hỏi văn bản. Nhập cả hai cookie trong tab **Cấu hình** để bật lịch sử hội thoại, tải tệp lên và chọn mô hình.
- **Lỗi Kết nối**: Đảm bảo cổng `8000` có thể truy cập được và tùy chọn `api_key` khớp chính xác với cấu hình trong Home Assistant.
- **Độ ổn định của phiên**: Nếu cookie thường xuyên hết hạn, hãy sử dụng Firefox để trích xuất cookie. Các phiên bản gần đây của các trình duyệt dựa trên Chromium sử dụng "Device Bound Session Credentials", giúp tăng cường bảo mật nhưng khiến cookie chỉ có hiệu lực trong vài giờ và không thể gia hạn.

---

## Lời cảm ơn

- Xây dựng dựa trên dự án xuất sắc Gemini-API từ [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API).
