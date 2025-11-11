# 📦 Hướng Dẫn Cài Đặt Nhanh

## Windows

### 1. Cài đặt Python
- Tải Python 3.8+ từ: https://www.python.org/downloads/
- Chọn "Add Python to PATH" khi cài đặt

### 2. Cài đặt Tesseract OCR
- Tải từ: https://github.com/UB-Mannheim/tesseract/wiki
- Cài đặt vào `C:\Program Files\Tesseract-OCR`
- Tải file ngôn ngữ Tiếng Việt:
  - Download `vie.traineddata` từ: https://github.com/tesseract-ocr/tessdata/raw/main/vie.traineddata
  - Copy vào: `C:\Program Files\Tesseract-OCR\tessdata\`

### 3. Cài đặt Poppler (cho PDF)
- Tải từ: https://github.com/oschwartz10612/poppler-windows/releases
- Giải nén và thêm folder `bin` vào PATH

### 4. Chạy ứng dụng
- Double click file `run.bat`
- Hoặc: Mở cmd và chạy `python main.py`

---

## macOS

### 1. Cài đặt Homebrew (nếu chưa có)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Cài đặt dependencies
```bash
# Python (nếu chưa có)
brew install python@3.11

# Tesseract OCR + Vietnamese language
brew install tesseract
brew install tesseract-lang

# Poppler (cho PDF)
brew install poppler
```

### 3. Chạy ứng dụng
```bash
chmod +x run.sh
./run.sh
```

---

## Linux (Ubuntu/Debian)

### 1. Cài đặt dependencies
```bash
# Update package list
sudo apt-get update

# Python 3 và pip
sudo apt-get install python3 python3-pip python3-venv

# Tesseract OCR + Vietnamese
sudo apt-get install tesseract-ocr tesseract-ocr-vie

# Poppler (cho PDF)
sudo apt-get install poppler-utils

# Tkinter (cho GUI)
sudo apt-get install python3-tk
```

### 2. Chạy ứng dụng
```bash
chmod +x run.sh
./run.sh
```

---

## Cấu Hình API Key

### Lấy Gemini API Key MIỄN PHÍ:
1. Truy cập: https://makersuite.google.com/app/apikey
2. Đăng nhập bằng tài khoản Google
3. Click "Create API Key"
4. Copy API key

### Cấu hình:
- Mở file `.env`
- Thay thế `your_api_key_here` bằng API key vừa lấy:
```
GEMINI_API_KEY=your_actual_api_key_here
```

---

## Kiểm Tra Cài Đặt

### Test Python:
```bash
python --version
# Hoặc
python3 --version
```

### Test Tesseract:
```bash
tesseract --version
```

### Test Poppler:
```bash
# Windows
pdfinfo -v

# Linux/macOS
pdfinfo -version
```

---

## Cài Đặt Thủ Công (không dùng script)

```bash
# 1. Tạo virtual environment
python3 -m venv venv

# 2. Activate (Linux/macOS)
source venv/bin/activate

# 2. Activate (Windows)
venv\Scripts\activate

# 3. Cài đặt packages
pip install --upgrade pip
pip install -r requirements.txt

# 4. Chạy ứng dụng
python main.py
```

---

## Xử Lý Lỗi

### Lỗi: "ModuleNotFoundError: No module named 'tkinter'"
**Linux:**
```bash
sudo apt-get install python3-tk
```

### Lỗi: "TesseractNotFoundError"
**Kiểm tra Tesseract đã cài đặt:**
```bash
tesseract --version
```

**Nếu chưa có, cài đặt theo hướng dẫn ở trên**

### Lỗi: "PDFInfoNotInstalledError"
**Cài đặt Poppler:**
- Windows: https://github.com/oschwartz10612/poppler-windows
- macOS: `brew install poppler`
- Linux: `sudo apt-get install poppler-utils`

---

## Cấu Trúc Sau Khi Cài Đặt

```
Hien/
├── venv/                   # Virtual environment
├── output/                 # File kết quả Excel
├── .env                    # API key (đã cấu hình)
└── [các file python]
```

---

## Chạy Lần Đầu

1. **Đảm bảo đã cài đặt đủ dependencies**
2. **Cấu hình API key trong file `.env`**
3. **Chạy ứng dụng:**
   - Windows: Double click `run.bat`
   - Linux/macOS: `./run.sh`
4. **Chọn folder chứa giấy tờ (PDF/JPG/PNG)**
5. **Click "BẮT ĐẦU XỬ LÝ"**
6. **Đợi xử lý xong và click "MỞ FILE KẾT QUẢ"**

---

## Hỗ Trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra file README.md
2. Xem mục "Xử Lý Lỗi Thường Gặp" trong README
3. Tạo Issue trên GitHub

**Chúc bạn sử dụng thành công!** 🎉
