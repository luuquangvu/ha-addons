# Giải pháp AI cho Home Assistant - Tích hợp Google Gemini & Công cụ Thông minh

[![Home Assistant App](https://img.shields.io/badge/Home%20Assistant-Add--on-blue?style=for-the-badge&logo=home-assistant)](https://github.com/luuquangvu/ha-addons)

**[ [🇺🇸 English](README.md) | 🇻🇳 Tiếng Việt ]**

Tích hợp các công nghệ trí tuệ nhân tạo tiên tiến vào hệ sinh thái Home Assistant của bạn. Kho lưu trữ này cung cấp các App chuyên biệt giúp mang đến AI tạo sinh (Generative AI), tự động hóa thông minh và các tích hợp nâng cao cho ngôi nhà thông minh.

## Nội dung Kho lưu trữ

- **Google Gemini cho Home Assistant (Gemini FastAPI)**
  - Tích hợp **Google Gemini** vào nhà thông minh hoàn toàn miễn phí. Đây là một cổng API tương thích với OpenAI sử dụng session cookie trình duyệt, giúp loại bỏ nhu cầu sử dụng Google Cloud API key. Ứng dụng hỗ trợ ghi nhớ lịch sử hội thoại, xử lý đa phương thức và cung cấp câu trả lời thời gian thực với Google Search ngay trong Home Assistant Assist.
  - **📖 Hướng dẫn Chi tiết:** [Xem hướng dẫn đầy đủ tại đây →](gemini-fastapi/README.vi.md)

## Hướng dẫn Cài đặt

Bạn có thể thêm kho lưu trữ này vào Home Assistant bằng một trong các phương pháp sau:

### 1. Phương pháp Tự động (Khuyến nghị)

Nhấp vào nút bên dưới để tự động thêm kho lưu trữ vào Assistant của bạn:

[![Mở Home Assistant của bạn và hiển thị hộp thoại thêm kho App Store với URL kho lưu trữ cụ thể được điền sẵn.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Fha-addons)

### 2. Phương pháp Thủ công

1. Trong Home Assistant, đi tới **Cấu hình > Apps > App Store**.
2. Nhấp vào **menu ba chấm** (⋮) ở góc trên bên phải và chọn **Repositories** (Kho lưu trữ).
3. Thêm URL kho lưu trữ: `https://github.com/luuquangvu/ha-addons`
4. Nhấp vào **Add** (Thêm) và chọn **Close** (Đóng).
5. Các App hiện có sẽ xuất hiện trong cửa hàng để bạn có thể cài đặt.

> [!TIP]
> Sau khi cài đặt một App, hãy nhấn **Start** (Bắt đầu) một lần để hệ thống tự động tạo các tệp cấu hình mặc định trước khi bạn bắt đầu chỉnh sửa.

## Bảo trì và Cập nhật

- **Cập nhật**: Home Assistant sẽ tự động kiểm tra định kỳ các bản cập nhật mới. Bạn cũng có thể nhấn nút **Reload** trong App Store để làm mới danh sách thủ công.
- **Gỡ bỏ**: Để xóa kho lưu trữ, hãy mở lại hộp thoại **Repositories**, chọn `luuquangvu/ha-addons` và nhấn **Remove**. Các App đã cài đặt sẽ không bị mất cho đến khi bạn gỡ cài đặt chúng thủ công.

---

## Hỗ trợ & Tài liệu Tham khảo

- Báo lỗi hoặc đóng góp ý kiến qua [GitHub Issues](https://github.com/luuquangvu/ha-addons/issues).
- Gemini FastAPI được xây dựng dựa trên dự án xuất sắc từ [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API).

## Giấy phép

Phát hành dưới Giấy phép MIT. Xem tệp [LICENSE](LICENSE) để biết thêm chi tiết.
