# FastAPI Automated Recruitment Screening System

Hệ thống sàng lọc tuyển dụng tự động sử dụng **FastAPI** và mô hình Transformer **all-MiniLM-L6-v2** để đánh giá mức độ phù hợp giữa ứng viên và công việc thông qua phân tích tương đồng ngữ nghĩa (Semantic Similarity).

---

## 🛠 1. Thông số kỹ thuật

- **Ngôn ngữ:** Python 3.13.3
- **Framework:** FastAPI 25.3
- **AI Model:** `all-MiniLM-L6-v2` (Sentence-Transformers)
- **Database:** PostgreSQL + `pgvector` (Lưu trữ và tìm kiếm tọa độ Vector)

---

## 2. Cài đặt môi trường

### Khởi tạo môi trường ảo (Virtual Environment)

```bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt venv (Windows)
venv\Scripts\activate

# Kích hoạt venv (Linux/Mac)
source venv/bin/activate
```

### Cài đặt thư viện

```bash
# Cài đặt toàn bộ thư viện từ file requirements
pip install -r requirements.txt

# Cài đặt thủ công các thư viện cốt lõi nếu cần
pip install fastapi[all] uvicorn sentence-transformers pgvector
```

## 3. Cấu hình Database & Docker (pgvector)

Dự án yêu cầu PostgreSQL tích hợp extension pgvector. Sử dụng Docker là giải pháp tối ưu để tránh việc cài đặt thủ công các file .dll phức tạp trên Windows.

### Bước 1: Giải phóng cổng kết nối (Cổng 5432)

Nếu bạn đang chạy PostgreSQL trực tiếp trên Windows, hãy tắt nó để Docker có thể sử dụng cổng này:

- Nhấn <mark>Win + R</mark>, gõ <mark>services.msc</mark> và nhấn **Enter**.

- Tìm dịch vụ PostgreSQL (ví dụ: postgresql-x64-17).

- Chuột phải vào nó và chọn <mark>Stop</mark>.

### Bước 2: Chạy Docker pgvector

Mở Terminal và chạy lệnh sau để khởi tạo server Postgres tích hợp sẵn Extension AI:

```bash
docker run --name my-postgres-vector \
  -e POSTGRES_PASSWORD=123456 \
  -e POSTGRES_DB=cv_evaluator_db \
  -p 5432:5432 \
  -d ankane/pgvector
```

### Bước 3: Dọn dẹp dữ liệu (Chạy trong pgAdmin)

Mở pgAdmin, kết nối vào server (localhost:5432) và chạy các lệnh sau trong Query Tool để làm sạch môi trường:

```sql
-- Kích hoạt extension Vector
CREATE EXTENSION IF NOT EXISTS vector;

-- Xóa các bảng và Type cũ để tránh lỗi xung đột khi Migration
DROP TABLE IF EXISTS "Hr", "Jobs", "CVs", "alembic_version" CASCADE;
DROP TYPE IF EXISTS userstatus, cvfiletype, jobstatus, educationlevel, batchstatus, embeddingtype CASCADE;
```

## 4. Cấu hình Migration (Alembic)

### Tự động hóa Import pgvector

Để tránh lỗi NameError: pgvector is not defined trong các file migration tự động sinh ra:

1. Mở file <mark>migrations/script.py.mako</mark>.

2. Chèn dòng sau vào phần đầu của các lệnh import:

```python
import pgvector.sqlalchemy
```

hoặc:

### Khai báo Models trong env.py

Đảm bảo file <mark>migrations/env.py</mark> đã load đủ Metadata của các Model:

```python
from app.core.database import Base
from app.models import *

target_metadata = Base.metadata
```

### Thực thi lệnh Migration

```bash
# Tạo file migration tự động
alembic revision --autogenerate -m "init tables"

# Cập nhật cấu trúc vào Database
alembic upgrade head

# Kiểm tra trạng thái hiện tại
alembic current
```

## 5. Vận hành & Kiểm tra

### Chạy Server FastAPI:

```bash
uvicorn app.main:app --reload --port 8080
```

### Chạy toàn bộ dự án:

```bash
docker compose up -d
```

#### Khi build, sửa code và muốn cập nhật vào Docker:

```bash
docker compose up --build -d
```

#### Khi bạn muốn dừng hoàn toàn:

```bash
docker compose down
```

### Quy trình cập nhập database trên môi trường đã build

#### 1. Tạo file migration mới (Revision):

```bash
docker-compose exec web alembic revision --autogenerate -m <"description_of_change">
```

#### 2. Kiểm tra file

Kiểm tra lần nữa file đã chỉnh sửa.

#### 3. Áp dụng vào DB:

```bash
docker-compose exec web alembic upgrade head
```

### Tài liệu API:

Swagger UI: [Swagger_docs](http://localhost:8080/docs)

### Kiểm tra kết nối Database:

```bash
python -m tests.test_db
```

- nho import model trong thu muc alembic/env.py

```bash
from app.models import resume, job, evaluation
sua lai import dong nay
```

- Tạo migration từ models

```bash
alembic revision --autogenerate -m "init tables"
```

- Apply migration (tạo bảng)

```bash
alembic upgrade head
```

- Check DB

```bash
alembic current
```

- cac buoc sua model khong can sua tren database

```bash
alembic revision --autogenerate -m "abc...."
alembic upgrade head
```

- Chạy docker có pgvector:

```bash
docker run --name my-postgres-vector -e POSTGRES_PASSWORD=12345 -p 5432:5432 -d ankane/pgvector
```
