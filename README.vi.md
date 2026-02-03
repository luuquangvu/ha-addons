# Kho Add-ons cho Home Assistant

[🇺🇸 English](README.md)

[![License](https://img.shields.io/github/license/luuquangvu/ha-addons)](LICENSE)

Các add-on tùy chỉnh giúp nâng cao khả năng của Home Assistant với các tính năng AI và các ý tưởng thử nghiệm khác. Mỗi add-on nằm trong một thư mục riêng với tài liệu, cấu hình và biểu tượng riêng, vì vậy bạn chỉ cần chọn những gì bạn cần.

## Nội dung kho lưu trữ

- **Gemini FastAPI**
  - Một wrapper tương thích với OpenAI cho Google Gemini, hoạt động thông qua cookie trình duyệt giúp loại bỏ nhu cầu sử dụng API key chính thức, cho phép sử dụng hoàn toàn miễn phí và không giới hạn. Các tính năng bao gồm lưu trữ hội thoại, tích hợp Google Search và bảo mật bằng API key tùy chọn. Người dùng Docker có thể dễ dàng triển khai độc lập theo hướng dẫn trong tài liệu.
  - Tài liệu: [gemini-fastapi/README.vi.md](gemini-fastapi/README.vi.md)

## Cài đặt (Cửa hàng Add-on)

Bạn có thể thêm kho lưu trữ này vào Home Assistant của mình bằng một trong các phương pháp sau:

### 1. Phương pháp tự động (Khuyên dùng)

Cách dễ nhất để thêm kho lưu trữ này là nhấp vào nút bên dưới, nút này sẽ hướng dẫn bạn qua quy trình một cách tự động:

[![Mở Home Assistant của bạn và hiển thị hộp thoại thêm kho add-on với URL kho lưu trữ cụ thể được điền sẵn.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Fha-addons)

### 2. Phương pháp thủ công

Nếu phương pháp tự động không hoạt động, bạn có thể thêm kho lưu trữ theo cách thủ công bằng các bước sau:

1. Trong Home Assistant, đi tới **Settings > Add-ons > Add-on Store** (Cài đặt > Add-ons > Cửa hàng Add-on).
2. Nhấp vào **menu ba chấm** (⋮) ở góc trên bên phải và chọn **Repositories** (Kho lưu trữ).
3. Sao chép và dán URL kho lưu trữ: `https://github.com/luuquangvu/ha-addons`
4. Nhấp vào **Add** (Thêm) và sau đó **Close** (Đóng) hộp thoại.
5. Các add-on của kho lưu trữ bây giờ sẽ có sẵn trong cửa hàng để cài đặt.

> [!TIP]
> Sau khi cài đặt một add-on, hãy nhấp vào **Start** (Bắt đầu) một lần để các tệp cấu hình mặc định được tạo ra trước khi chỉnh sửa.

## Cập nhật / Gỡ bỏ

- Home Assistant tự động kiểm tra kho lưu trữ này để tìm các bản cập nhật. Bạn cũng có thể nhấn nút **Reload** (Tải lại) trong Cửa hàng Add-on để lấy các phiên bản mới nhất theo yêu cầu.
- Để xóa kho lưu trữ, hãy mở lại hộp thoại **Repositories**, chọn `luuquangvu/ha-addons` và nhấp vào **Remove** (Gỡ bỏ). Các add-on đã cài đặt vẫn sẽ tồn tại cho đến khi bạn gỡ cài đặt chúng.

## Hỗ trợ & Đóng góp

- Tìm thấy lỗi, có ý tưởng hoặc muốn đóng góp? [Mở một issue](https://github.com/luuquangvu/ha-addons/issues) hoặc gửi pull request.
- Gemini FastAPI dựa trên công trình xuất sắc từ [Nativu5/Gemini-FastAPI](https://github.com/Nativu5/Gemini-FastAPI).

## Giấy phép

Được phát hành theo Giấy phép MIT. Xem tệp [LICENSE](LICENSE) để biết chi tiết.
