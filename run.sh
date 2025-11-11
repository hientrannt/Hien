#!/bin/bash
# Script chạy ứng dụng trích xuất giấy tờ

echo "======================================"
echo "🔍 HỆ THỐNG TRÍCH XUẤT GIẤY TỜ"
echo "======================================"
echo ""

# Kiểm tra Python
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 chưa được cài đặt!"
    echo "Vui lòng cài đặt Python 3.8 trở lên"
    exit 1
fi

echo "✅ Python version: $(python3 --version)"

# Kiểm tra dependencies
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Tạo virtual environment..."
    python3 -m venv venv
fi

echo ""
echo "🔄 Kích hoạt virtual environment..."
source venv/bin/activate

echo ""
echo "📦 Cài đặt dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "🚀 Khởi động ứng dụng..."
echo ""
python3 main.py

deactivate
