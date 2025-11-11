"""
Giao diện GUI cho ứng dụng xử lý giấy tờ
"""
import os
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
from datetime import datetime
import subprocess
import platform

from pdf_processor import DocumentProcessor
from gemini_extractor import GeminiExtractor
from excel_writer import ExcelWriter
from config import SUPPORTED_FORMATS


class DocumentProcessorApp:
    """Ứng dụng GUI xử lý giấy tờ"""

    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Hệ Thống Trích Xuất Giấy Tờ - Gemini AI")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Biến
        self.folder_path = tk.StringVar()
        self.api_key = tk.StringVar()
        self.processing = False
        self.output_file = None

        # Processors
        self.doc_processor = DocumentProcessor()
        self.gemini_extractor = None

        # Setup UI
        self._setup_ui()

    def _setup_ui(self):
        """Thiết lập giao diện"""

        # ===== HEADER =====
        header_frame = tk.Frame(self.root, bg="#4472C4", height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🔍 HỆ THỐNG TRÍCH XUẤT GIẤY TỜ",
            font=("Arial", 18, "bold"),
            bg="#4472C4",
            fg="white"
        )
        title_label.pack(pady=10)

        subtitle_label = tk.Label(
            header_frame,
            text="Sử dụng Google Gemini AI + OCR | Hỗ trợ PDF, JPG, PNG",
            font=("Arial", 10),
            bg="#4472C4",
            fg="white"
        )
        subtitle_label.pack()

        # ===== API KEY SECTION =====
        api_frame = tk.LabelFrame(self.root, text="⚙️  Cấu hình API", font=("Arial", 10, "bold"), padx=10, pady=10)
        api_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(api_frame, text="Gemini API Key:", font=("Arial", 9)).grid(row=0, column=0, sticky="w", padx=5)
        api_entry = tk.Entry(api_frame, textvariable=self.api_key, width=60, show="*")
        api_entry.grid(row=0, column=1, padx=5, pady=5)

        # Load API key từ config
        from config import GEMINI_API_KEY
        self.api_key.set(GEMINI_API_KEY)

        # ===== FOLDER SELECTION =====
        folder_frame = tk.LabelFrame(self.root, text="📁 Chọn Thư Mục Chứa Giấy Tờ", font=("Arial", 10, "bold"), padx=10, pady=10)
        folder_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Entry(folder_frame, textvariable=self.folder_path, width=60, state="readonly").grid(row=0, column=0, padx=5, pady=5)

        btn_browse = tk.Button(
            folder_frame,
            text="📂 Chọn Thư Mục",
            command=self._browse_folder,
            bg="#5B9BD5",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            padx=10,
            pady=5
        )
        btn_browse.grid(row=0, column=1, padx=5)

        # ===== FILE LIST =====
        file_frame = tk.LabelFrame(self.root, text="📄 Danh Sách File", font=("Arial", 10, "bold"), padx=10, pady=10)
        file_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Treeview
        columns = ("Tên File", "Loại", "Kích Thước")
        self.file_tree = ttk.Treeview(file_frame, columns=columns, show="headings", height=8)

        self.file_tree.heading("Tên File", text="Tên File")
        self.file_tree.heading("Loại", text="Loại")
        self.file_tree.heading("Kích Thước", text="Kích Thước")

        self.file_tree.column("Tên File", width=400)
        self.file_tree.column("Loại", width=80)
        self.file_tree.column("Kích Thước", width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        self.file_tree.configure(yscroll=scrollbar.set)

        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ===== PROGRESS =====
        progress_frame = tk.Frame(self.root, padx=10, pady=5)
        progress_frame.pack(fill=tk.X, padx=20)

        self.progress = ttk.Progressbar(progress_frame, mode='determinate', length=400)
        self.progress.pack(fill=tk.X, pady=5)

        self.status_label = tk.Label(progress_frame, text="Sẵn sàng", font=("Arial", 9), fg="green")
        self.status_label.pack()

        # ===== LOG WINDOW =====
        log_frame = tk.LabelFrame(self.root, text="📋 Log Xử Lý", font=("Arial", 10, "bold"), padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, wrap=tk.WORD, font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # ===== BUTTONS =====
        button_frame = tk.Frame(self.root, padx=10, pady=10)
        button_frame.pack(fill=tk.X, padx=20, pady=10)

        self.btn_start = tk.Button(
            button_frame,
            text="▶️  BẮT ĐẦU XỬ LÝ",
            command=self._start_processing,
            bg="#70AD47",
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            padx=20,
            pady=10
        )
        self.btn_start.pack(side=tk.LEFT, padx=5)

        self.btn_open = tk.Button(
            button_frame,
            text="📊 MỞ FILE KẾT QUẢ",
            command=self._open_output_file,
            bg="#FFC000",
            fg="black",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.btn_open.pack(side=tk.LEFT, padx=5)

        btn_clear = tk.Button(
            button_frame,
            text="🗑️  XÓA LOG",
            command=self._clear_log,
            bg="#C5C5C5",
            fg="black",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            padx=20,
            pady=10
        )
        btn_clear.pack(side=tk.RIGHT, padx=5)

    def _browse_folder(self):
        """Chọn thư mục"""
        folder = filedialog.askdirectory(title="Chọn thư mục chứa giấy tờ")
        if folder:
            self.folder_path.set(folder)
            self._load_files(folder)
            self._log(f"✅ Đã chọn thư mục: {folder}")

    def _load_files(self, folder):
        """Load danh sách file từ thư mục"""
        # Clear tree
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)

        # Scan files
        files = []
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):
                ext = os.path.splitext(file)[1].lower()
                if ext in SUPPORTED_FORMATS:
                    size = os.path.getsize(file_path)
                    size_str = self._format_size(size)
                    files.append((file, ext, size_str))

        # Add to tree
        for file, ext, size in files:
            self.file_tree.insert("", tk.END, values=(file, ext, size))

        self._log(f"📂 Tìm thấy {len(files)} file hợp lệ")

    def _format_size(self, size):
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def _log(self, message):
        """Ghi log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def _clear_log(self):
        """Xóa log"""
        self.log_text.delete(1.0, tk.END)

    def _update_status(self, message, color="black"):
        """Cập nhật status"""
        self.status_label.config(text=message, fg=color)
        self.root.update_idletasks()

    def _update_progress(self, value):
        """Cập nhật progress bar"""
        self.progress['value'] = value
        self.root.update_idletasks()

    def _start_processing(self):
        """Bắt đầu xử lý"""
        if self.processing:
            messagebox.showwarning("Cảnh báo", "Đang xử lý, vui lòng đợi!")
            return

        if not self.folder_path.get():
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục!")
            return

        if not self.api_key.get():
            messagebox.showerror("Lỗi", "Vui lòng nhập Gemini API Key!")
            return

        # Chạy trong thread riêng
        self.processing = True
        self.btn_start.config(state=tk.DISABLED)
        self.btn_open.config(state=tk.DISABLED)

        thread = threading.Thread(target=self._process_files, daemon=True)
        thread.start()

    def _process_files(self):
        """Xử lý tất cả file trong thư mục"""
        try:
            self._log("\n" + "="*60)
            self._log("🚀 BẮT ĐẦU XỬ LÝ")
            self._log("="*60)

            # Khởi tạo Gemini extractor
            self.gemini_extractor = GeminiExtractor(api_key=self.api_key.get())

            # Khởi tạo Excel writer
            excel_writer = ExcelWriter()
            self._log(f"📊 File output: {excel_writer.get_output_file()}")

            # Lấy danh sách file
            folder = self.folder_path.get()
            files = []
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                if os.path.isfile(file_path):
                    ext = os.path.splitext(file)[1].lower()
                    if ext in SUPPORTED_FORMATS:
                        files.append(file_path)

            if not files:
                self._log("❌ Không tìm thấy file nào!")
                return

            total_files = len(files)
            self._log(f"📁 Tổng số file: {total_files}")

            # Thống kê
            stats = {
                'total': total_files,
                'success': 0,
                'error': 0,
                'GPKD': 0,
                'GPP': 0,
                'KDD': 0,
                'CCCD': 0
            }

            # Xử lý từng file
            for idx, file_path in enumerate(files, 1):
                try:
                    self._update_status(f"Đang xử lý {idx}/{total_files}...", "blue")
                    self._update_progress(int((idx - 1) / total_files * 100))

                    self._log(f"\n📄 [{idx}/{total_files}] {os.path.basename(file_path)}")

                    # Trích xuất dữ liệu
                    result = self.gemini_extractor.extract_single_file(
                        self.doc_processor,
                        file_path
                    )

                    if result['success']:
                        documents = result['documents']
                        self._log(f"✅ Tìm thấy {len(documents)} giấy tờ")

                        # Ghi vào Excel
                        for doc in documents:
                            write_result = excel_writer.write_document(doc)
                            if write_result['success']:
                                stats[doc['type']] += 1
                                self._log(f"   ✓ {doc['type']}: {write_result['message']}")
                            else:
                                self._log(f"   ✗ {write_result['message']}")

                        stats['success'] += 1
                    else:
                        self._log(f"❌ Lỗi: {result.get('error', 'Unknown')}")
                        stats['error'] += 1

                except Exception as e:
                    self._log(f"❌ Lỗi xử lý file: {str(e)}")
                    stats['error'] += 1

            # Lưu Excel
            self._update_status("Đang lưu file Excel...", "blue")
            excel_writer.save()
            self.output_file = excel_writer.get_output_file()

            # Hoàn thành
            self._update_progress(100)
            self._update_status("✅ Hoàn thành!", "green")

            # Hiển thị kết quả
            self._log("\n" + "="*60)
            self._log("📊 KẾT QUẢ TỔNG HỢP")
            self._log("="*60)
            self._log(f"✅ Thành công: {stats['success']}/{stats['total']}")
            self._log(f"❌ Lỗi: {stats['error']}/{stats['total']}")
            self._log(f"\n📋 PHÂN LOẠI:")
            if stats['GPKD'] > 0:
                self._log(f"   • GPKD: {stats['GPKD']}")
            if stats['GPP'] > 0:
                self._log(f"   • GPP: {stats['GPP']}")
            if stats['KDD'] > 0:
                self._log(f"   • KDD: {stats['KDD']}")
            if stats['CCCD'] > 0:
                self._log(f"   • CCCD: {stats['CCCD']}")

            self._log(f"\n🔗 File kết quả: {self.output_file}")
            self._log("="*60)

            # Enable nút mở file
            self.btn_open.config(state=tk.NORMAL)

            messagebox.showinfo("Thành công", f"Đã xử lý xong!\n\nFile kết quả:\n{self.output_file}")

        except Exception as e:
            self._log(f"\n❌ LỖI NGHIÊM TRỌNG: {str(e)}")
            self._update_status("❌ Có lỗi xảy ra!", "red")
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra:\n{str(e)}")

        finally:
            self.processing = False
            self.btn_start.config(state=tk.NORMAL)

    def _open_output_file(self):
        """Mở file output"""
        if not self.output_file or not os.path.exists(self.output_file):
            messagebox.showerror("Lỗi", "File không tồn tại!")
            return

        try:
            # Mở file theo hệ điều hành
            if platform.system() == 'Windows':
                os.startfile(self.output_file)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', self.output_file])
            else:  # Linux
                subprocess.call(['xdg-open', self.output_file])

            self._log(f"📂 Đã mở file: {self.output_file}")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở file:\n{str(e)}")


def main():
    """Chạy ứng dụng"""
    root = tk.Tk()
    app = DocumentProcessorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
