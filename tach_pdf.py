import sys
import os
import re
import ctypes
from ctypes import wintypes
import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader, PdfWriter

def hide_console():
    # Hide the console window if running from a shortcut or explorer
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, 0) # SW_HIDE = 0

def ask_open_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Chon file PDF can tach",
        filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
    )
    root.destroy()
    return file_path

def ask_directory():
    root = tk.Tk()
    root.withdraw()
    dir_path = filedialog.askdirectory(
        title="Chon thu muc de luu cac file sau khi tach"
    )
    root.destroy()
    return dir_path

def main():
    print("========================================")
    print("  TachPDF (Standalone version)")
    print("========================================")
    
    input_path = ""
    output_dir = ""
    
    if len(sys.argv) < 2:
        print("[GUI] Dang mo cua so chon file...")
        input_path = ask_open_file()
        if not input_path:
            print("[LOI] Da huy chon file!")
            input("Nhan Enter de thoat...")
            sys.exit(1)
    else:
        input_path = sys.argv[1]
        
    if len(sys.argv) >= 3:
        output_dir = sys.argv[2]
    else:
        print("[GUI] Dang mo cua so chon thu muc luu...")
        output_dir = ask_directory()
        if not output_dir:
            print("[INFO] Khong chon thu muc luu, se luu mac dinh ra man hinh Desktop.")
            output_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            
    # Tu dong tao thu muc con voi ten file pdf de luu
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_dir = os.path.join(output_dir, f"{base_name}_DaTach")
            
    if not os.path.exists(input_path):
        print(f"[LOI] Khong tim thay file: {input_path}")
        input("Nhan Enter de thoat...")
        sys.exit(1)
        
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"[INFO] File input: {input_path}")
    print(f"[INFO] Thu muc output: {output_dir}\n")
    
    print("Dang doc file...")
    try:
        reader = PdfReader(input_path)
    except Exception as e:
        print(f"[LOI] Khong the doc file PDF: {e}")
        input("Nhan Enter de thoat...")
        sys.exit(1)
        
    total_pages = len(reader.pages)
    print(f"Tong so trang: {total_pages}")
    
    room_pattern = re.compile(r'\b(\d{3})\.\d[TD]\b')
    room_pages = {}
    unknown_pages = []
    
    print("Dang phan tich so phong...")
    for i in range(total_pages):
        text = reader.pages[i].extract_text()
        groups = set(room_pattern.findall(text))
        
        if not groups:
            unknown_pages.append(i)
        else:
            for group in groups:
                if group not in room_pages:
                    room_pages[group] = []
                room_pages[group].append(i)
        
        pct = (i + 1) * 100 // total_pages
        print(f"\r  Phan tich: {i+1}/{total_pages} ({pct}%)", end='', flush=True)
    print()
    
    print(f"Tim thay {len(room_pages)} nhom phong")
    if unknown_pages:
        print(f"{len(unknown_pages)} trang khong co so phong")
        
    print("Dang tach va luu file PDF...")
    file_count = 0
    total_files = len(room_pages) + (1 if unknown_pages else 0)
    
    for room in sorted(room_pages.keys()):
        pages = sorted(set(room_pages[room]))
        writer = PdfWriter()
        for page_idx in pages:
            writer.add_page(reader.pages[page_idx])
            
        filename = f"Phong_{room}.pdf"
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'wb') as f:
            writer.write(f)
            
        file_count += 1
        pct = file_count * 100 // total_files
        print(f"\r  Tach PDF: {file_count}/{total_files} ({pct}%)", end='', flush=True)
        
    if unknown_pages:
        writer = PdfWriter()
        for page_idx in unknown_pages:
            writer.add_page(reader.pages[page_idx])
            
        output_path = os.path.join(output_dir, "Phong_khac.pdf")
        with open(output_path, 'wb') as f:
            writer.write(f)
        file_count += 1
        
    print("\n\nHOAN THANH! Da tach thanh {} file PDF".format(file_count))
    print("Luu tai:", output_dir, "\n")
    
    for f in sorted(os.listdir(output_dir)):
        if f.endswith('.pdf'):
            size = os.path.getsize(os.path.join(output_dir, f))
            print(f"  {f} ({size // 1024} KB)")
            
    input("\nNhan Enter de thoat...")

if __name__ == "__main__":
    main()
