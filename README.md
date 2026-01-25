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
+ Model: 
```bash
pip install -U sentence-transformers
```

