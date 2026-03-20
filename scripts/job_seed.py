from decimal import Decimal
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.job import Job
from app.models.enum import JobStatus, EducationLevel as EducationLevelEnum

def seed_jobs(db: Session):
    jobs_data = [
        {
            "Title": "Fullstack Developer Intern",
            "Description": "Tham gia phát triển các dự án web application sử dụng Next.js cho frontend và FastAPI cho backend.",
            "RequirementsText": "Kiến thức cơ bản về Python, JavaScript/TypeScript. Ưu tiên sinh viên năm cuối chuyên ngành HTTT.",
            "MinExperience": Decimal("0.0"),
            "EducationLevel": EducationLevelEnum.BACHELOR,
            "Status": JobStatus.OPEN
        },
        # ... các vị trí khác giữ nguyên như bạn đã viết ...
        {
            "Title": "System Administrator",
            "Description": "Quản trị hệ thống máy chủ và mạng cho doanh nghiệp.",
            "RequirementsText": "Kinh nghiệm quản trị Windows/Linux Server. Hiểu biết về bảo mật hệ thống.",
            "MinExperience": Decimal("2.5"),
            "EducationLevel": EducationLevelEnum.BACHELOR,
            "Status": JobStatus.DRAFT
        }
    ]

    print("Đang bắt đầu seed dữ liệu Job...")
    for job_item in jobs_data:
        existing_job = db.query(Job).filter(Job.Title == job_item["Title"]).first()
        if not existing_job:
            new_job = Job(**job_item)
            db.add(new_job)
            print(f" - Đã thêm: {job_item['Title']}")
        else:
            print(f" - Đã tồn tại: {job_item['Title']} (Bỏ qua)")
    
    db.commit()
    print("--- Seed dữ liệu Job hoàn tất! ---")

# --- PHẦN QUAN TRỌNG ĐỂ CHẠY ĐƯỢC PYTHON -M ---
if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_jobs(db)
    finally:
        db.close()