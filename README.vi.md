# Kho AI & Apps cho Home Assistant - Tích hợp Gemini Miễn phí

**[ [🇺🇸 English](README.md) | 🇻🇳 Tiếng Việt ]**

[![License](https://img.shields.io/github/license/luuquangvu/ha-addons)](LICENSE)

Nâng tầm ngôi nhà thông minh của bạn với **Google Gemini cho Home Assistant** và các công cụ AI mạnh mẽ khác. Kho lưu trữ này cung cấp các Apps (tên cũ là add-ons) tùy chỉnh, giúp mang đến các tính năng AI tiên tiến, tự động hóa thử nghiệm và các tích hợp thông minh vào hệ sinh thái Home Assistant của bạn.

## Nội dung kho lưu trữ

- **Gemini FastAPI (Google Gemini cho Home Assistant)**
  - Tích hợp **Google Gemini** vào nhà thông minh hoàn toàn miễn phí. Đây là một wrapper tương thích với OpenAI sử dụng cookie trình duyệt, giúp loại bỏ nhu cầu sử dụng API key trả phí. Ứng dụng cho phép chat AI không giới hạn, lưu lịch sử hội thoại và trả lời dựa trên Google Search ngay trong Home Assistant Assist.
  - Hướng dẫn chi tiết: [gemini-fastapi/README.vi.md](gemini-fastapi/README.vi.md)

## Cài đặt (Cửa hàng Apps)

Bạn có thể thêm kho lưu trữ này vào Home Assistant của mình bằng một trong các phương pháp sau:

### 1. Phương pháp tự động (Khuyên dùng)

Cách dễ nhất để thêm kho lưu trữ này là nhấp vào nút bên dưới, nút này sẽ hướng dẫn bạn qua quy trình một cách tự động:

[![Mở Home Assistant của bạn và hiển thị hộp thoại thêm kho add-on với URL kho lưu trữ cụ thể được điền sẵn.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Fha-addons)

### 2. Phương pháp thủ công

Nếu phương pháp tự động không hoạt động, bạn có thể thêm kho lưu trữ theo cách thủ công bằng các bước sau:

1. Trong Home Assistant, đi tới **Settings > Apps > App Store** (Cài đặt > Apps > Cửa hàng Apps).
2. Nhấp vào **menu ba chấm** (⋮) ở góc trên bên phải và chọn **Repositories** (Kho lưu trữ).
3. Sao chép và dán URL kho lưu trữ: `https://github.com/luuquangvu/ha-addons`
4. Nhấp vào **Add** (Thêm) và sau đó **Close** (Đóng) hộp thoại.
5. Các Apps của kho lưu trữ bây giờ sẽ có sẵn trong cửa hàng để cài đặt.

> [!TIP]
> Sau khi cài đặt một App, hãy nhấp vào **Start** (Bắt đầu) một lần để các tệp cấu hình mặc định được tạo ra trước khi chỉnh sửa.

## Cập nhật / Gỡ bỏ

- Home Assistant tự động kiểm tra kho lưu trữ này để tìm các bản cập nhật. Bạn cũng có thể nhấn nút **Reload** (Tải lại) trong Cửa hàng Apps để lấy các phiên bản mới nhất theo yêu cầu.
- Để xóa kho lưu trữ, hãy mở lại hộp thoại **Repositories**, chọn `luuquangvu/ha-addons` và nhấp vào **Remove** (Gỡ bỏ). Các Apps đã cài đặt vẫn sẽ tồn tại cho đến khi bạn gỡ cài đặt chúng.

## Hỗ trợ & Đóng góp

- Tìm thấy lỗi, có ý tưởng hoặc muốn đóng góp? [Mở một issue](https://github.com/luuquangvu/ha-addons/issues) hoặc gửi pull request.
- Gemini FastAPI dựa trên công trình xuất sắc từ [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API).

## Giấy phép

Được phát hành theo Giấy phép MIT. Xem tệp [LICENSE](LICENSE) để biết chi tiết.
