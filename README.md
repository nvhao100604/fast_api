# FastAPI project

Hệ thống sàng lọc tuyển dụng tự động sử dụng FastAPI và mô hình transformer all-MiniLM-L6-v2 để đánh giá mức độ phù hợp giữa ứng viên và công việc thông qua phân tích tương đồng ngữ nghĩa.

## Thông tin phiên bản:

- Python 3.13.3
- FastAPI 25.3

## Hướng dẫn sử dụng:

- Chạy:

```bash
uvicorn app.main:app --reload --port 8080
```

- Mở:
  [Swagger API Documentation](http://localhost:8080/docs)

## Cài đặt:

```bash
pip install fastapi[all]
```

```bash
python -m venv venv
```

- Model:

```bash
pip install -U sentence-transformers
```

download requirements.txt : de cai dat cac thu vien

```bash
pip install -r requirements.txt
```

- Database: Chạy lệnh để tạo db trong PostgreSQL

```bash
create database cv_evaluator_db
```

- Chạy file test db connection:

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
