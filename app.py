import sys
import os
import fitz
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def split_pdf(master_file):
    try:
        doc = fitz.open(master_file)
        current_room = None
        room_pages = {}

        # Scan each page
        for i in range(len(doc)):
            text = doc[i].get_text('text')
            
            # Find patterns like 101.1T, 203.2D...
            # This captures the room number dynamically
            matches = re.findall(r'\b(\d{3,4})\.[1-9][A-Z]+\b', text)
            
            if matches:
                # Take the first match as the room number for this page
                current_room = matches[0]
                
            if current_room:
                if current_room not in room_pages:
                    room_pages[current_room] = []
                room_pages[current_room].append(i)

        if not room_pages:
            messagebox.showerror("Lỗi", "Không tìm thấy bất kỳ mã phòng nào trong file này!")
            return

        # Prepare output directory - Ask user for location
        chosen_dir = filedialog.askdirectory(title="Chọn thư mục để lưu các file sau khi tách")
        if not chosen_dir:
            # User cancelled directory selection
            messagebox.showwarning("Đã hủy", "Bạn chưa chọn nơi lưu file. Quá trình tách bị hủy.")
            return
            
        base_name = os.path.splitext(os.path.basename(master_file))[0]
        output_dir = os.path.join(chosen_dir, f"{base_name}_DaTach")
        os.makedirs(output_dir, exist_ok=True)
        
        # Split and save
        for room, pages in room_pages.items():
            new_doc = fitz.open()
            for page_num in pages:
                new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
                
            new_filename = os.path.join(output_dir, f"{base_name}_{room}.pdf")
            # Use garbage=3 and deflate=True to optimize file size
            new_doc.save(new_filename, garbage=3, deflate=True)
            new_doc.close()

        doc.close()
        messagebox.showinfo("Thành công", f"Đã tách thành {len(room_pages)} file thành công!\nCác file được lưu tại thư mục:\n{output_dir}")

    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

def main():
    # Hide the main tkinter window
    root = tk.Tk()
    root.withdraw()
    
    file_path = None
    
    # Check if a file was drag-and-dropped onto the executable
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Otherwise, open a file dialog
        file_path = filedialog.askopenfilename(
            title="Chọn file PDF cần tách",
            filetypes=[("PDF files", "*.pdf")]
        )
        
    if file_path and os.path.exists(file_path):
        split_pdf(file_path)
    else:
        # User canceled or file doesn't exist
        pass

if __name__ == "__main__":
    main()
