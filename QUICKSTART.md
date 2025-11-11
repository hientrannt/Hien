# 🚀 HƯỚNG DẪN SỬ DỤNG NHANH

## 📥 BƯỚC 1: GIẢI NÉN FILE

Giải nén file `Hien_Document_Extractor.zip` vào thư mục bạn muốn.

Sau khi giải nén, bạn sẽ có thư mục `Hien/` chứa tất cả file cần thiết.

---

## ⚙️ BƯỚC 2: CÀI ĐẶT

### Windows:

1. **Cài đặt Python 3.8+** (nếu chưa có)
   - Tải tại: https://www.python.org/downloads/
   - ✅ Nhớ check "Add Python to PATH"

2. **Cài đặt Tesseract OCR**
   - Tải tại: https://github.com/UB-Mannheim/tesseract/wiki
   - Cài đặt vào `C:\Program Files\Tesseract-OCR`
   - Tải file ngôn ngữ tiếng Việt:
     * https://github.com/tesseract-ocr/tessdata/raw/main/vie.traineddata
     * Copy vào: `C:\Program Files\Tesseract-OCR\tessdata\`

3. **Cài đặt Poppler** (để xử lý PDF)
   - Tải tại: https://github.com/oschwartz10612/poppler-windows/releases
   - Giải nén và thêm folder `bin` vào PATH

4. **Chạy ứng dụng**
   - Double-click file `run.bat`
   - Hoặc mở CMD và gõ: `python main.py`

### Linux/Ubuntu:

```bash
# Cài đặt dependencies
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv python3-tk
sudo apt-get install tesseract-ocr tesseract-ocr-vie
sudo apt-get install poppler-utils

# Chạy ứng dụng
chmod +x run.sh
./run.sh
```

### macOS:

```bash
# Cài đặt Homebrew (nếu chưa có)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Cài đặt dependencies
brew install python@3.11
brew install tesseract tesseract-lang
brew install poppler

# Chạy ứng dụng
chmod +x run.sh
./run.sh
```

---

## 🔑 BƯỚC 3: CẤU HÌNH API KEY

1. **Lấy Gemini API Key MIỄN PHÍ:**
   - Truy cập: https://makersuite.google.com/app/apikey
   - Đăng nhập Google
   - Click "Create API Key"
   - Copy API key

2. **Cấu hình:**
   - Mở file `.env` trong thư mục `Hien/`
   - Thay `your_api_key_here` bằng API key của bạn:
   ```
   GEMINI_API_KEY=AIzaSy...your_key_here
   ```

---

## 🎯 BƯỚC 4: SỬ DỤNG

1. Chạy ứng dụng:
   ```bash
   python main.py
   ```

2. Giao diện sẽ hiện ra:
   - Click "📂 Chọn Thư Mục"
   - Chọn folder chứa file PDF/JPG/PNG của bạn
   - Kiểm tra danh sách file được tìm thấy
   - Click "▶️ BẮT ĐẦU XỬ LÝ"
   - Đợi xử lý xong
   - Click "📊 MỞ FILE KẾT QUẢ"

3. File Excel kết quả sẽ được lưu trong folder `output/`

---

## 📋 LOẠI GIẤY TỜ HỖ TRỢ

✅ GPKD - Giấy phép đăng ký kinh doanh
✅ GPP - Giấy phép hành nghề dược (cá nhân)
✅ KDD - Giấy chứng nhận kinh doanh dược (cơ sở)
✅ CCCD - Căn cước công dân

---

## 📂 FILE ĐỊNH DẠNG HỖ TRỢ

✅ PDF (nhiều trang)
✅ JPG / JPEG
✅ PNG

---

## ❓ XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi: "Python not found"
➡️ Cài đặt Python 3.8+ và thêm vào PATH

### Lỗi: "Tesseract not found"
➡️ Cài đặt Tesseract OCR theo hướng dẫn trên

### Lỗi: "Failed to convert PDF"
➡️ Cài đặt Poppler cho hệ điều hành của bạn

### Lỗi: "Invalid API Key"
➡️ Kiểm tra lại API key trong file `.env`

### Lỗi: "ModuleNotFoundError"
➡️ Chạy: `pip install -r requirements.txt`

---

## 📞 HỖ TRỢ

Nếu gặp khó khăn:
1. Đọc file `README.md` để biết hướng dẫn chi tiết
2. Đọc file `INSTALL.md` để biết cách cài đặt cho từng hệ điều hành
3. Kiểm tra phần "Xử Lý Lỗi Thường Gặp" trong README.md

---

## 🎉 CHÚC BẠN SỬ DỤNG THÀNH CÔNG!

**Powered by Python + Google Gemini AI + OCR**
