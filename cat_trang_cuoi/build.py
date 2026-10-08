import subprocess
import sys
import os

def build_exe():
    print("Đang cài đặt các thư viện cần thiết (pypdf, pyinstaller)...")
    # Cài đặt thư viện tự động
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf", "pyinstaller"])
    
    print("\nBắt đầu đóng gói thành file .exe...")
    # Lệnh đóng gói:
    # --noconsole: Không hiển thị cửa sổ dòng lệnh đen khi chạy exe
    # --onefile: Gộp tất cả vào 1 file exe duy nhất
    # --clean: Dọn dẹp bộ nhớ tạm trước khi build
    subprocess.check_call([
        sys.executable, "-m", "PyInstaller", 
        "--noconsole", 
        "--onefile", 
        "--clean",
        "pdf_trimmer.py"
    ])
    
    print("\n===============================================")
    print("HOÀN TẤT! File .exe của bạn đã được tạo thành công.")
    print("Hãy mở thư mục 'dist' vừa xuất hiện để lấy file pdf_trimmer.exe")
    print("===============================================")

if __name__ == "__main__":
    build_exe()