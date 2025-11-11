"""
Module trích xuất dữ liệu từ giấy tờ sử dụng Google Gemini AI
"""
import json
import time
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL, PROMPT_TEMPLATE


class GeminiExtractor:
    """Trích xuất dữ liệu từ hình ảnh giấy tờ bằng Gemini AI"""

    def __init__(self, api_key=None):
        self.api_key = api_key or GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(GEMINI_MODEL)

    def extract_from_images(self, image_data_list, max_retries=3):
        """
        Trích xuất dữ liệu từ danh sách hình ảnh

        Args:
            image_data_list: List các dict {
                'image_base64': base64 string,
                'mime_type': 'image/png' hoặc 'image/jpeg',
                'page_num': số trang
            }
            max_retries: Số lần thử lại nếu lỗi

        Returns:
            list: Danh sách các giấy tờ đã trích xuất
                [{'type': 'GPKD', 'data': {...}}, ...]
        """
        try:
            # Chuẩn bị nội dung gửi cho Gemini
            contents = []

            # Thêm tất cả hình ảnh
            for img_data in image_data_list:
                contents.append({
                    'mime_type': img_data['mime_type'],
                    'data': img_data['image_base64']
                })

            # Thêm prompt
            contents.append(PROMPT_TEMPLATE)

            print(f"🤖 Đang phân tích {len(image_data_list)} trang với Gemini AI...")

            # Gọi API với retry logic
            for attempt in range(max_retries):
                try:
                    response = self.model.generate_content(contents)

                    # Lấy text response
                    if not response.text:
                        raise Exception("Không nhận được phản hồi từ Gemini AI")

                    text_response = response.text.strip()
                    print(f"📝 Response từ AI: {text_response[:200]}...")

                    # Parse JSON
                    documents = self._parse_json_response(text_response)

                    # Đảm bảo là mảng
                    if not isinstance(documents, list):
                        documents = [documents]

                    print(f"✅ Đã trích xuất {len(documents)} giấy tờ")

                    return documents

                except Exception as e:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt  # Exponential backoff
                        print(f"⚠️  Lỗi lần {attempt + 1}, thử lại sau {wait_time}s: {str(e)}")
                        time.sleep(wait_time)
                    else:
                        raise

        except Exception as e:
            print(f"❌ Lỗi trích xuất dữ liệu: {str(e)}")
            raise

    def _parse_json_response(self, text):
        """Parse JSON từ response của AI"""
        # Loại bỏ markdown code blocks
        text = text.replace('```json', '').replace('```', '').strip()

        # Tìm JSON array hoặc object
        try:
            # Thử parse trực tiếp
            return json.loads(text)
        except json.JSONDecodeError:
            # Thử tìm JSON trong text
            import re

            # Tìm JSON array
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if match:
                return json.loads(match.group(0))

            # Tìm JSON object
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group(0))

            raise Exception(f"Không thể parse JSON từ response: {text[:200]}")

    def validate_document(self, document):
        """Kiểm tra tính hợp lệ của document"""
        if not isinstance(document, dict):
            return False, "Document không phải là dict"

        if 'type' not in document:
            return False, "Thiếu trường 'type'"

        if 'data' not in document:
            return False, "Thiếu trường 'data'"

        valid_types = ['GPKD', 'GPP', 'KDD', 'CCCD']
        if document['type'] not in valid_types:
            return False, f"Loại giấy tờ không hợp lệ: {document['type']}"

        return True, "OK"

    def extract_single_file(self, file_processor, file_path):
        """
        Xử lý một file hoàn chỉnh

        Args:
            file_processor: Instance của DocumentProcessor
            file_path: Đường dẫn file

        Returns:
            dict: {
                'success': True/False,
                'file': file_path,
                'documents': [...],
                'error': error message (nếu có)
            }
        """
        try:
            # 1. Xử lý file thành hình ảnh
            print(f"\n{'='*60}")
            print(f"📄 Đang xử lý: {file_path}")
            print(f"{'='*60}")

            image_data_list = file_processor.process_file(file_path)

            # 2. Trích xuất dữ liệu với Gemini
            documents = self.extract_from_images(image_data_list)

            # 3. Validate kết quả
            valid_documents = []
            for doc in documents:
                is_valid, msg = self.validate_document(doc)
                if is_valid:
                    valid_documents.append(doc)
                else:
                    print(f"⚠️  Bỏ qua document không hợp lệ: {msg}")

            return {
                'success': True,
                'file': file_path,
                'documents': valid_documents,
                'total_pages': len(image_data_list)
            }

        except Exception as e:
            return {
                'success': False,
                'file': file_path,
                'error': str(e),
                'documents': []
            }


# Test function
if __name__ == "__main__":
    from pdf_processor import DocumentProcessor

    processor = DocumentProcessor()
    extractor = GeminiExtractor()

    test_file = "test.pdf"
    if os.path.exists(test_file):
        result = extractor.extract_single_file(processor, test_file)
        print("\n" + "="*60)
        print("📊 KẾT QUẢ:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
