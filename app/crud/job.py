from typing import Optional

from sqlalchemy.orm import Session

from app.models.job import Job

def get_job_by_name(db: Session, name: str) -> Optional[Job]:
    """Tìm job theo tên (không phân biệt hoa thường)."""
    return db.query(Job).filter(Job.Title.ilike(name)).first()