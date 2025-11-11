"""
Cấu hình cho ứng dụng xử lý giấy tờ
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCKm2zzSIKXempK-eLIr5csWKxrnmfFxqs")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

# Định dạng file hỗ trợ
SUPPORTED_FORMATS = ['.pdf', '.jpg', '.jpeg', '.png']

# Tên các sheet Excel
SHEET_NAMES = {
    "GPKD": "GPKD",
    "GPP": "GPP",
    "KDD": "KDD",
    "CCCD": "CCCD"
}

# Thư mục output
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Cấu hình OCR
OCR_LANG = 'vie+eng'  # Tiếng Việt + Tiếng Anh

# Prompt template cho Gemini
PROMPT_TEMPLATE = """
Phân tích file này và trích xuất TẤT CẢ các giấy tờ.

NHẬN DIỆN 4 LOẠI GIẤY TỜ:
1. GPKD: Giấy chứng nhận đăng ký doanh nghiệp (có mã số thuế, tên công ty, vốn điều lệ)
2. GPP: Giấy phép hành nghề dược CÁ NHÂN (có số GPP với dấu "/")
3. KDD: Giấy chứng nhận đủ điều kiện kinh doanh dược CƠ SỞ (có số hiệu với "/" và "-")
4. CCCD: Căn cước công dân (có số CCCD 12 chữ số, ảnh chân dung)

LUÔN TRẢ VỀ MẢNG JSON với format sau:
[
  {
    "type": "GPKD",
    "data": {
      "mST": "mã số thuế",
      "soGPDKKD": "số GPĐKKD",
      "ngayDangKy": "dd/mm/yyyy",
      "lanThayDoi": "số lần",
      "ngayThayDoi": "dd/mm/yyyy",
      "tenDonvi": "tên công ty",
      "diaChi": "địa chỉ",
      "dienThoai": "điện thoại",
      "emailDV": "email",
      "vonDieuLe": "số tiền không dấu",
      "hoVaTen": "người đại diện",
      "chucDanh": "chức danh",
      "gioiTinh": "Nam/Nữ",
      "sinhNgay": "dd/mm/yyyy",
      "quocTich": "Việt Nam",
      "loaiGiayTo": "CCCD/CMND",
      "soGiayTo": "số",
      "ngayCap": "dd/mm/yyyy",
      "noiCap": "nơi cấp",
      "diaChiThuongTru": "địa chỉ"
    }
  },
  {
    "type": "GPP",
    "data": {
      "so_gpp": "số GPP",
      "co_so": "tên cơ sở",
      "tru_so": "địa chỉ trụ sở",
      "dia_chi": "địa chỉ kinh doanh",
      "nguoi_quan_ly_chuyen_mon": "họ tên",
      "pham_vi_kinh_doanh": "phạm vi",
      "thoi_han": "thời hạn",
      "noi_cap": "nơi cấp",
      "ngay_cap": "dd/mm/yyyy"
    }
  },
  {
    "type": "KDD",
    "data": {
      "so_hieu": "số hiệu KDD",
      "ten_co_so": "tên cơ sở",
      "tru_so": "trụ sở chính",
      "ten_dia_diem_kinh_doanh": "tên địa điểm",
      "dia_chi_kinh_doanh": "địa chỉ",
      "ho_va_ten": "người chịu trách nhiệm",
      "trinh_do_chuyen_mon": "trình độ",
      "chung_chi_hanh_nghe_duoc": "số chứng chỉ",
      "cap_ngay": "dd/mm/yyyy",
      "du_dieu_kien_kinh_doanh_duoc_loai_hinh": "loại hình",
      "pham_vi_kinh_doanh": "phạm vi",
      "thoi_han": "thời hạn",
      "noi_cap": "nơi cấp",
      "ngay_cap": "dd/mm/yyyy"
    }
  },
  {
    "type": "CCCD",
    "data": {
      "so_cccd": "12 chữ số",
      "ho_va_ten": "họ và tên",
      "ngay_sinh": "dd/mm/yyyy",
      "gioi_tinh": "Nam/Nữ",
      "quoc_tich": "Việt Nam",
      "que_quan": "quê quán",
      "noi_thuong_tru": "địa chỉ",
      "co_gia_tri_den": "dd/mm/yyyy"
    }
  }
]

QUY TẮC:
- Trả về MẢNG JSON chứa TẤT CẢ giấy tờ tìm được
- Nếu chỉ có 1 giấy tờ vẫn trả về mảng [{}]
- Trường không có dữ liệu để ""
- CHỈ trả về JSON thuần, KHÔNG có text khác
- Ngày tháng format dd/mm/yyyy
- Số tiền/vốn điều lệ không có dấu phân cách
"""
