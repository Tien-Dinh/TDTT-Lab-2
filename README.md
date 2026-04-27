# [LAB - 2] APPLICATION PROGRAMMING INTERFACE AND FIREBASE STUDIO

## 1. Thông tin sinh viên
* **Họ và tên:** Đinh Võ Thủy Tiên
* **MSSV:** 24120148
* **Môn học:** Tư duy tính toán
* **Lớp học:** CQ2024/3

## 2. Thông tin ứng dụng (Notes App)
* **Tính năng chính:** Ứng dụng Quản lý ghi chú cá nhân.
* **Công nghệ sử dụng:**
  * **Frontend:** Streamlit
  * **Backend:** FastAPI
  * **Cơ sở dữ liệu & Xác thực:** Firebase (Firestore Database & Email/Password Authentication).
* **Mô tả chức năng:** Hệ thống cho phép người dùng đăng ký và đăng nhập tài khoản bằng Email/Password thông qua Firebase. Sau khi xác thực thành công, người dùng có thể thực hiện các thao tác: xem danh sách ghi chú, thêm mới, chỉnh sửa và xóa ghi chú. Dữ liệu được lưu trữ trực tuyến và cô lập theo từng tài khoản người dùng trên Firestore.

## 3. Hướng dẫn cài đặt môi trường

**Yêu cầu hệ thống:** Đã cài đặt `Python 3.11.x` hoặc `Python 3.12.x` (bản 64-bit Stable), đã thiết lập sẵn dự án Firebase (Authentication - Email/Password, Firestore, Realtime Database) và tạo thư mục .streamlit cùng cấp với thư mục frontend/backend để tạo file secrets.toml chứa các khóa của dự án [firebase_client], [firebase_admin].

1. Mở `Terminal` tại thư mục gốc của dự án.
2. Tạo môi trường ảo (virtual environment) bằng lệnh:
   ```bash
    # Windows:
    # Kích hoạt venv
    python -m venv venv
    # Vào file venv để xem có thư mục bin hay Scripts rồi chọn dòng lệnh tương ứng
    .\venv\bin\Activate.ps1
    .\venv\Scripts\Activate.ps1
    
    ```
3. Chạy lệnh cài đặt thư viện:
   ```bash
   pip install -r requirements.txt
   ```

## 4. Hướng dẫn chạy chương trình
1. Chạy backend:
    * Mở `Terminal` ở tại thư mục gốc của dự án, chạy dòng lệnh di chuyển vào thư mục chứa code backend:
   ```bash
   cd backend/app
   ```
   * Chạy server:
   ```bash
   python -m uvicorn main:app --reload --port 8000
   ```
   * Hệ thống sẽ hoạt động tại địa chỉ: `http://127.0.0.1:8000`.
   * Tài liệu API tương tác (Swagger UI) có sẵn tại: `http://127.0.0.1:8000/docs`.
2. Chạy frontend:
    * Mở một tab `Terminal` mới tại thư mục gốc của dự án khác với tab `Terminal` đang chạy backend, chạy dòng lệnh di chuyển vào thư mục chứa code frontend:
   ```bash
   cd frontend
   ```
   * Chạy giao diện:
   ```bash
   python -m streamlit run app.py
   ```
   * Hệ thống giao diện sẽ tự động mở trên trình duyệt tại: `http://localhost:8501`.
## 5. Liên kết đến video demo
