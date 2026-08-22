# BeHome HKA SplitPDF

Ứng dụng nhỏ gọn giúp tự động quét nội dung file tổng PDF, nhận diện số phòng (VD: 101, 102...) và cắt các trang tương ứng thành từng file PDF nhỏ chứa thông tin của phòng đó.

## Cách sử dụng (Với file exe)
1. Chạy file `TachPDF.exe` hoặc kéo thả (drag & drop) một file PDF vào nó.
2. Hộp thoại sẽ hiện ra cho phép bạn chọn nơi lưu kết quả.
3. Chờ giây lát, ứng dụng sẽ tách ra các file nhỏ (VD: `BILL-HKA-T082026_101.pdf`).

## Source Code
Mã nguồn chính nằm ở file `app.py`.
Yêu cầu thư viện:
- `PyMuPDF`
- `PyInstaller` (nếu muốn build thành exe)

### Cách build từ mã nguồn:
1. Cài đặt Python
2. Mở cửa sổ lệnh tại thư mục này và chạy: `.\build.ps1`
3. File `.exe` sẽ được lưu vào thư mục `dist`.
