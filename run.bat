@echo off
REM Script chạy ứng dụng trích xuất giấy tờ trên Windows

echo ======================================
echo 🔍 HỆ THỐNG TRÍCH XUẤT GIẤY TỜ
echo ======================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python chưa được cài đặt!
    echo Vui lòng cài đặt Python 3.8 trở lên
    pause
    exit /b 1
)

echo ✅ Python đã được cài đặt
python --version

REM Kiểm tra virtual environment
if not exist "venv\" (
    echo.
    echo 📦 Tạo virtual environment...
    python -m venv venv
)

echo.
echo 🔄 Kích hoạt virtual environment...
call venv\Scripts\activate.bat

echo.
echo 📦 Cài đặt dependencies...
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q

echo.
echo 🚀 Khởi động ứng dụng...
echo.
python main.py

deactivate
pause
