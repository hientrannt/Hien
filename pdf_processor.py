"""
Module xử lý PDF và hình ảnh
Hỗ trợ: PDF, JPG, PNG
Sử dụng OCR để chuyển hình ảnh thành text
"""
import os
import base64
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
from config import OCR_LANG, OUTPUT_DIR


class DocumentProcessor:
    """Xử lý các loại tài liệu: PDF, JPG, PNG"""

    def __init__(self):
        self.temp_dir = os.path.join(OUTPUT_DIR, "temp")
        os.makedirs(self.temp_dir, exist_ok=True)

    def get_file_type(self, file_path):
        """Xác định loại file"""
        ext = os.path.splitext(file_path)[1].lower()
        return ext

    def pdf_to_images(self, pdf_path):
        """Chuyển PDF thành list các hình ảnh"""
        try:
            images = convert_from_path(pdf_path, dpi=300)
            return images
        except Exception as e:
            raise Exception(f"Lỗi chuyển đổi PDF: {str(e)}")

    def image_to_base64(self, image):
        """Chuyển PIL Image thành base64 string"""
        import io

        if isinstance(image, str):
            # Nếu là đường dẫn file
            with open(image, 'rb') as f:
                image_bytes = f.read()
        else:
            # Nếu là PIL Image
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            image_bytes = buffer.getvalue()

        return base64.b64encode(image_bytes).decode('utf-8')

    def ocr_image(self, image):
        """OCR hình ảnh để lấy text (dự phòng)"""
        try:
            if isinstance(image, str):
                image = Image.open(image)

            # OCR với Tesseract
            text = pytesseract.image_to_string(image, lang=OCR_LANG)
            return text.strip()
        except Exception as e:
            print(f"⚠️  Cảnh báo OCR: {str(e)}")
            return ""

    def process_file(self, file_path):
        """
        Xử lý file và trả về danh sách hình ảnh (dạng base64)

        Returns:
            list: Danh sách dict {
                'image_base64': base64 string,
                'ocr_text': text từ OCR (optional),
                'page_num': số trang (nếu là PDF)
            }
        """
        file_type = self.get_file_type(file_path)
        results = []

        if file_type == '.pdf':
            # Xử lý PDF: chuyển thành nhiều hình ảnh
            print(f"📄 Đang xử lý PDF: {os.path.basename(file_path)}")
            images = self.pdf_to_images(file_path)

            for idx, image in enumerate(images, 1):
                print(f"  📄 Trang {idx}/{len(images)}")
                image_base64 = self.image_to_base64(image)
                ocr_text = self.ocr_image(image)

                results.append({
                    'image_base64': image_base64,
                    'ocr_text': ocr_text,
                    'page_num': idx,
                    'mime_type': 'image/png'
                })

        elif file_type in ['.jpg', '.jpeg', '.png']:
            # Xử lý hình ảnh đơn
            print(f"🖼️  Đang xử lý hình ảnh: {os.path.basename(file_path)}")
            image_base64 = self.image_to_base64(file_path)
            ocr_text = self.ocr_image(file_path)

            # Xác định mime type
            mime_type = 'image/jpeg' if file_type in ['.jpg', '.jpeg'] else 'image/png'

            results.append({
                'image_base64': image_base64,
                'ocr_text': ocr_text,
                'page_num': 1,
                'mime_type': mime_type
            })

        else:
            raise Exception(f"Định dạng file không được hỗ trợ: {file_type}")

        return results

    def cleanup(self):
        """Dọn dẹp file tạm"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            os.makedirs(self.temp_dir, exist_ok=True)


# Test function
if __name__ == "__main__":
    processor = DocumentProcessor()

    # Test với file mẫu
    test_file = "test.pdf"  # Thay bằng file thật
    if os.path.exists(test_file):
        results = processor.process_file(test_file)
        print(f"\n✅ Đã xử lý {len(results)} trang/hình")
        for r in results:
            print(f"  - Trang {r['page_num']}: {len(r['ocr_text'])} ký tự OCR")
