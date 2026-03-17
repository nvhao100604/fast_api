
from typing import Optional

from sqlalchemy.orm import Session

# from app.api.v1.schemas import 
from app.models.User import User, UserRole
from app.models.cv_embedding import CVEmbedding
from app.models.job import Job, JobEmbedding

# ─── READ ────────────────────────────────────────────────────

def get_job_embedding_by_id(db: Session, job_id: int) -> Optional[JobEmbedding]:
    """Tìm job embedding theo primary key. Trả None nếu không tồn tại."""
    return db.query(JobEmbedding).filter(JobEmbedding.Id == job_id).first()

def get_cv_embedding_by_id(db: Session, cv_id: int) -> Optional[CVEmbedding]:
    """Tìm CV embedding theo primary key. Trả None nếu không tồn tại."""
    return db.query(CVEmbedding).filter(CVEmbedding.Id == cv_id).first()

def get_job_embeddings(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    role: Optional[UserRole] = None,
    is_active: Optional[bool] = None,
) -> tuple[list[User], int]:
    query = db.query(xUser)

    if role is not None:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    total = query.count()
    users = (
        query
        .order_by(User.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return users, total

def get_cv_embeddings(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    role: Optional[UserRole] = None,
    is_active: Optional[bool] = None,
) -> tuple[list[User], int]:
    query = db.query(xUser)

    if role is not None:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    total = query.count()
    users = (
        query
        .order_by(User.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return users, total


# ─── CREATE ──────────────────────────────────────────────────

def create_job_embedding(db: Session, **kwargs) -> JobEmbedding:
    job_embedding = JobEmbedding(**kwargs)
    db.add(job_embedding)
    db.commit()
    db.refresh(user) 
    return user


# ─── UPDATE ──────────────────────────────────────────────────

def update_user(db: Session, user: User, **kwargs) -> User:
    for field, value in kwargs.items():
        if value is not None:
            setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def save_user(db: Session, user: User) -> User:
    db.commit()
    db.refresh(user)
    return user


# ─── DELETE ──────────────────────────────────────────────────

def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()