import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from pypdf import PdfReader, PdfWriter

def main():
    # Khởi tạo tkinter và ẩn cửa sổ console/cửa sổ chính
    root = tk.Tk()
    root.withdraw()

    # Mở trình quản lý tệp để chọn file PDF đầu vào
    input_pdf_path = filedialog.askopenfilename(
        title="Chọn file PDF cần cắt trang cuối",
        filetypes=[("PDF files", "*.pdf")]
    )
    
    if not input_pdf_path:
        return  # Thoát nếu người dùng bấm Cancel

    try:
        reader = PdfReader(input_pdf_path)
        total_pages = len(reader.pages)

        # Kiểm tra nếu file chỉ có 1 trang hoặc rỗng
        if total_pages <= 1:
            messagebox.showerror("Lỗi", "File PDF chỉ có 1 trang hoặc rỗng, không thể cắt bỏ trang cuối.")
            return

        # Cắt trang cuối bằng cách thêm từ trang đầu đến trang áp chót
        writer = PdfWriter()
        for i in range(total_pages - 1):
            writer.add_page(reader.pages[i])

        # Lấy đường dẫn thư mục Documents của máy tính làm mặc định
        documents_path = str(Path.home() / "Documents")
        
        # Đề xuất tên file mới (thêm chữ _dacat)
        original_filename = Path(input_pdf_path).stem
        default_out_name = f"{original_filename}_dacat.pdf"

        # Mở trình quản lý tệp chọn nơi lưu
        output_pdf_path = filedialog.asksaveasfilename(
            title="Lưu file PDF mới",
            initialdir=documents_path,
            initialfile=default_out_name,
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )

        if not output_pdf_path:
            return  # Thoát nếu người dùng bấm Cancel

        # Ghi ra file mới
        with open(output_pdf_path, "wb") as output_file:
            writer.write(output_file)

        messagebox.showinfo("Thành công", f"Đã cắt trang cuối và lưu file tại:\n{output_pdf_path}")

    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi trong quá trình xử lý:\n{str(e)}")

if __name__ == "__main__":
    main()
