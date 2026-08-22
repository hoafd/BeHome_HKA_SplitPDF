# Script tự động cài đặt thư viện và đóng gói ứng dụng thành file .exe

Write-Host "Bắt đầu quá trình build app..." -ForegroundColor Cyan

# 1. Cài đặt hoặc cập nhật thư viện cần thiết
Write-Host "Cài đặt thư viện PyMuPDF và PyInstaller..." -ForegroundColor Yellow
pip install pymupdf pyinstaller

# Kiểm tra xem app.py có tồn tại không
if (-Not (Test-Path -Path "app.py")) {
    Write-Host "Lỗi: Không tìm thấy file app.py trong thư mục hiện tại!" -ForegroundColor Red
    exit
}

# 2. Xóa các thư mục build cũ (nếu có) để bản build được sạch
if (Test-Path -Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path -Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path -Path "TachPDF.spec") { Remove-Item -Force "TachPDF.spec" }

# 3. Đóng gói ứng dụng
Write-Host "Đang tiến hành đóng gói (có thể mất 1-2 phút)..." -ForegroundColor Yellow
python -m PyInstaller --onefile --windowed --clean -n TachPDF app.py

# 4. Kiểm tra kết quả
if (Test-Path -Path "dist\TachPDF.exe") {
    Write-Host "Đóng gói THÀNH CÔNG!" -ForegroundColor Green
    Write-Host "File app của bạn nằm tại: dist\TachPDF.exe" -ForegroundColor Green
} else {
    Write-Host "Có lỗi xảy ra trong quá trình đóng gói!" -ForegroundColor Red
}

Write-Host "Hoàn tất!" -ForegroundColor Cyan
