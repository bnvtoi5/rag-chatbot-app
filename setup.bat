@echo off
title CAI DAT HE THONG RAG
chcp 65001 > nul
cls

echo ============================================================
echo   BƯỚC 1: KHỞI TẠO MÔI TRƯỜNG VÀ CÀI ĐẶT THƯ VIỆN (1 LẦN DUY NHẤT)
echo ============================================================
echo.

:: 1. Kiểm tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [LỖI] Không tìm thấy Python trên máy tính! Vui lòng cài đặt Python 3.10+.
    pause
    exit /b
)

:: 2. Khởi tạo venv
if not exist .venv (
    echo [*] Đang khởi tạo môi trường ảo Python (.venv)...
    python -m venv .venv
)

:: 3. Kích hoạt venv
call .venv\Scripts\activate

:: 4. Nhập API Key
if not exist .env (
    echo ------------------------------------------------------------
    set /p api_key="👉 Vui lòng nhập hoặc dán GROQ_API_KEY của bạn: "
    echo GROQ_API_KEY=%api_key% > .env
    echo [OK] Đã lưu cấu hình tài khoản!
    echo ------------------------------------------------------------
    echo.
)

:: 5. Cài đặt thư viện theo lệnh tối ưu của bạn
echo [*] Đang cài đặt các thư viện văn bản (Vui lòng chờ)...
pip install -r requirements.txt --no-cache-dir -v
if %errorlevel% neq 0 (
    echo [LỖI] Cài đặt thất bại! Vui lòng kiểm tra mạng.
    pause
    exit /b
)

echo.
echo ============================================================
echo [THÀNH CÔNG] Đã setup xong! Bạn có thể tắt file này.
echo Từ bây giờ, bạn chỉ cần click file "2_Chay_Ung_Dung.bat" để dùng app.
echo ============================================================
echo.
pause