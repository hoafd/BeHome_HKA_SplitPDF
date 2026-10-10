@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo   Dong goi TachPDF thanh 1 file duy nhat
echo ========================================
echo.

if not exist "icon.ico" (
    echo [LOI] Khong tim thay file caikeo.ico!
    echo Vui long tai 1 file icon hinh cai keo ^(.ico^) va doi ten thanh caikeo.ico
    echo de cung thu muc voi file build.bat roi chay lai.
    echo.
    pause
    exit /b 1
)

echo [INFO] Kiem tra va cai dat PyInstaller, PyPDF2...
python -m pip install pyinstaller PyPDF2

echo [1/2] Dang dong goi... (qua trinh nay co the mat vai phut)
python -m PyInstaller --onefile --console --icon="icon.ico" --name=TachPDF tach_pdf.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo [LOI] Dong goi that bai!
    pause
    exit /b 1
)

echo.
echo [2/2] Dong goi thanh cong!
echo.
echo   -^> File exe doc lap (chay khong can Python):
echo      dist\TachPDF.exe
echo.
pause
