# Giải pháp AI cho Home Assistant

[![Home Assistant App](https://img.shields.io/badge/Home%20Assistant-App-blue?style=for-the-badge&logo=home-assistant)](https://github.com/luuquangvu/ha-addons)

**[🇺🇸 English](README.md) | 🇻🇳 Tiếng Việt**

Tích hợp các công nghệ trí tuệ nhân tạo tiên tiến vào hệ sinh thái Home Assistant của bạn. Kho lưu trữ này cung cấp các App chuyên biệt giúp mang đến AI tạo sinh (Generative AI), xử lý giọng nói cục bộ (STT & TTS), tự động hóa thông minh và các tích hợp nâng cao cho ngôi nhà thông minh.

## Nội dung Kho lưu trữ

- **Google Gemini cho Home Assistant (Gemini FastAPI)**
  - Tích hợp **Google Gemini** vào nhà thông minh hoàn toàn miễn phí. Đây là một cổng API tương thích với OpenAI sử dụng session cookie trình duyệt, giúp loại bỏ nhu cầu sử dụng Google Cloud API key. Ứng dụng hỗ trợ ghi nhớ lịch sử hội thoại, xử lý đa phương thức và cung cấp câu trả lời thời gian thực với Google Search ngay trong Home Assistant Assist.
  - **📖 Hướng dẫn Chi tiết:** [Xem hướng dẫn đầy đủ tại đây →](gemini-fastapi/README.vi.md)

- **Giọng nói tiếng Việt cho Home Assistant (Wyoming Vietnamese)**
  - Mang giọng nói tiếng Việt đến Assist mà vẫn chạy hoàn toàn trên thiết bị của bạn. App cung cấp cả nhận diện giọng nói và tổng hợp giọng nói qua một cổng Wyoming Protocol duy nhất, với 20 giọng tiếng Việt, không cần tài khoản đám mây và không cần API key.
  - **📖 Hướng dẫn Chi tiết:** [Xem hướng dẫn đầy đủ tại đây →](wyoming-vietnamese/README.vi.md)

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
> Cách cấu hình và hành vi ở lần khởi động đầu tiên phụ thuộc vào từng App (ví dụ: **Gemini FastAPI** sẽ tạo các tệp cấu hình mặc định ở lần chạy đầu, trong khi **Wyoming Vietnamese** sẽ tải về các mô hình nhận diện và giọng đọc). Vui lòng tham khảo tài liệu chi tiết của từng App để biết hướng dẫn cụ thể.

## Bảo trì và Cập nhật

- **Cập nhật**: Home Assistant sẽ tự động kiểm tra định kỳ các bản cập nhật mới. Bạn cũng có thể nhấn nút **Reload** trong App Store để làm mới danh sách thủ công.
- **Gỡ bỏ**: Để xóa kho lưu trữ, hãy mở lại hộp thoại **Repositories**, chọn `luuquangvu/ha-addons` và nhấn **Remove**. Các App đã cài đặt sẽ không bị mất cho đến khi bạn gỡ cài đặt chúng thủ công.

---

## Hỗ trợ & Lời cảm ơn

- **Hỗ trợ**: Báo lỗi hoặc đóng góp ý kiến qua [GitHub Issues](https://github.com/luuquangvu/ha-addons/issues).
- **Lời cảm ơn**:
  - **Gemini FastAPI**: Xây dựng dựa trên dự án [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API).
  - **Wyoming Vietnamese**: Sử dụng mô hình và thư viện từ [nghimestudio/nghitts](https://github.com/nghimestudio/nghitts), [hynt](https://huggingface.co/hynt), [k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) và [Wyoming Protocol](https://github.com/OHF-Voice/wyoming).

## Giấy phép

Phát hành dưới Giấy phép MIT. Xem tệp [LICENSE](LICENSE) để biết thêm chi tiết.
