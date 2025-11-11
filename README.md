# 🔍 Hệ Thống Trích Xuất Giấy Tờ

Ứng dụng Python tự động trích xuất thông tin từ giấy tờ sử dụng **Google Gemini AI** và **OCR**.

## ✨ Tính Năng

- 🤖 **Tự động nhận diện** 4 loại giấy tờ:
  - **GPKD**: Giấy phép đăng ký kinh doanh
  - **GPP**: Giấy phép hành nghề dược (cá nhân)
  - **KDD**: Giấy chứng nhận đủ điều kiện kinh doanh dược (cơ sở)
  - **CCCD**: Căn cước công dân

- 📄 **Hỗ trợ nhiều định dạng**:
  - PDF (nhiều trang)
  - JPG/JPEG
  - PNG

- 🎯 **Trích xuất thông minh**:
  - Kết hợp OCR + Gemini AI
  - Tự động phân tích và nhận diện loại giấy tờ
  - Trích xuất tất cả thông tin chi tiết

- 📊 **Xuất Excel tự động**:
  - Tạo sheet riêng cho từng loại giấy tờ
  - Format đẹp, dễ đọc
  - Tự động mở file kết quả

- 🖥️ **Giao diện đẹp**:
  - Tkinter GUI hiện đại
  - Progress bar theo dõi tiến trình
  - Log chi tiết
  - Dễ sử dụng

## 📋 Yêu Cầu Hệ Thống

- Python 3.8+
- Tesseract OCR
- Google Gemini API Key

## 🚀 Cài Đặt

### 1. Clone Repository

```bash
git clone <repository-url>
cd Hien
```

### 2. Cài Đặt Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Cài Đặt Tesseract OCR

#### Windows:
1. Download từ: https://github.com/UB-Mannheim/tesseract/wiki
2. Cài đặt và thêm vào PATH
3. Download Vietnamese language data:
   - Tải `vie.traineddata` từ https://github.com/tesseract-ocr/tessdata
   - Copy vào `C:\Program Files\Tesseract-OCR\tessdata\`

#### macOS:
```bash
brew install tesseract
brew install tesseract-lang
```

#### Linux:
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-vie
```

### 4. Cấu Hình API Key

Mở file `.env` và thay đổi API key:

```bash
GEMINI_API_KEY=your_api_key_here
```

**Lấy API Key miễn phí tại:** https://makersuite.google.com/app/apikey

## 📖 Hướng Dẫn Sử Dụng

### Chạy Ứng Dụng

```bash
python main.py
```

### Các Bước Xử Lý

1. **Nhập API Key** (nếu chưa có trong `.env`)
2. **Chọn Thư Mục** chứa file giấy tờ (PDF/JPG/PNG)
3. **Kiểm tra danh sách file** được tìm thấy
4. **Nhấn "BẮT ĐẦU XỬ LÝ"**
5. **Theo dõi tiến trình** qua Progress Bar và Log
6. **Nhấn "MỞ FILE KẾT QUẢ"** khi hoàn thành

### Kết Quả

File Excel sẽ được lưu trong thư mục `output/` với format:
```
output/KetQua_YYYYMMDD_HHMMSS.xlsx
```

Mỗi loại giấy tờ sẽ có sheet riêng:
- **GPKD**: Thông tin doanh nghiệp
- **GPP**: Giấy phép hành nghề
- **KDD**: Giấy chứng nhận kinh doanh
- **CCCD**: Căn cước công dân

## 📁 Cấu Trúc Project

```
Hien/
├── main.py                 # Entry point
├── gui_app.py             # Giao diện GUI
├── pdf_processor.py       # Xử lý PDF và hình ảnh
├── gemini_extractor.py    # Trích xuất dữ liệu với Gemini AI
├── excel_writer.py        # Ghi dữ liệu vào Excel
├── config.py              # Cấu hình
├── requirements.txt       # Python dependencies
├── .env                   # API keys (không commit)
├── .env.example          # Mẫu file .env
├── .gitignore            # Git ignore
├── README.md             # Tài liệu
└── output/               # Thư mục chứa kết quả
```

## 🔧 Cấu Hình Nâng Cao

### Thay Đổi Mô Hình Gemini

Mở file `config.py` và thay đổi:

```python
GEMINI_MODEL = "gemini-2.0-flash-exp"  # hoặc "gemini-pro-vision"
```

### Thay Đổi Ngôn Ngữ OCR

Mở file `config.py` và thay đổi:

```python
OCR_LANG = 'vie+eng'  # Tiếng Việt + Tiếng Anh
```

### Tùy Chỉnh Prompt

Mở file `config.py` và chỉnh sửa `PROMPT_TEMPLATE` theo nhu cầu.

## 🐛 Xử Lý Lỗi Thường Gặp

### Lỗi: "Tesseract not found"
- **Nguyên nhân**: Chưa cài đặt Tesseract OCR
- **Giải pháp**: Cài đặt Tesseract theo hướng dẫn ở trên

### Lỗi: "Invalid API Key"
- **Nguyên nhân**: API Key không hợp lệ
- **Giải pháp**: Kiểm tra lại API Key trong file `.env`

### Lỗi: "Failed to convert PDF"
- **Nguyên nhân**: Thiếu poppler (cho pdf2image)
- **Giải pháp**:
  - Windows: Download poppler từ https://github.com/oschwartz10612/poppler-windows
  - macOS: `brew install poppler`
  - Linux: `sudo apt-get install poppler-utils`

### Lỗi: "Permission denied" khi mở file Excel
- **Nguyên nhân**: File Excel đang mở
- **Giải pháp**: Đóng file Excel trước khi xử lý

## 📊 Ví Dụ Output

### GPKD Sheet
| MST | Tên đơn vị | Địa chỉ | Vốn điều lệ | ... |
|-----|-----------|---------|-------------|-----|
| 0123456789 | CÔNG TY ABC | Hà Nội | 1000000000 | ... |

### CCCD Sheet
| Số CCCD | Họ và tên | Ngày sinh | Giới tính | ... |
|---------|-----------|-----------|-----------|-----|
| 001234567890 | NGUYỄN VĂN A | 01/01/1990 | Nam | ... |

## 🤝 Đóng Góp

Mọi đóng góp đều được chào đón! Vui lòng:

1. Fork project
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📝 License

Dự án này được phát triển cho mục đích học tập và nghiên cứu.

## 🙏 Credits

- **Google Gemini AI**: https://ai.google.dev/
- **Tesseract OCR**: https://github.com/tesseract-ocr/tesseract
- **OpenPyXL**: https://openpyxl.readthedocs.io/

## 📧 Liên Hệ

Nếu có bất kỳ câu hỏi nào, vui lòng tạo Issue trên GitHub.

---

**Made with ❤️ by Python + Gemini AI**