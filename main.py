#!/usr/bin/env python3
"""
Hệ Thống Trích Xuất Giấy Tờ - Main Entry Point
Sử dụng Gemini AI + OCR để tự động nhận diện và trích xuất dữ liệu
"""
import sys
import os

# Thêm thư mục hiện tại vào Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gui_app import main

    if __name__ == "__main__":
        print("="*60)
        print("🔍 HỆ THỐNG TRÍCH XUẤT GIẤY TỜ")
        print("   Powered by Gemini AI + OCR")
        print("="*60)
        print("\n🚀 Đang khởi động giao diện...\n")

        # Chạy GUI
        main()

except ImportError as e:
    print(f"❌ Lỗi import: {e}")
    print("\n💡 Vui lòng cài đặt các thư viện cần thiết:")
    print("   pip install -r requirements.txt")
    sys.exit(1)

except Exception as e:
    print(f"❌ Lỗi khởi động: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
