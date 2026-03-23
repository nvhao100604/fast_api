from typing import List, Optional, Tuple
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func

from app.models.application import Application, ApplicationHistory, ApplicationStatus
from app.api.v1.schemas.application_schemas import ApplicationCreate


# ── Application ───────────────────────────────────────────────────────────────

def get_application_by_id(db: Session, application_id: int) -> Optional[Application]:
    return db.execute(
        select(Application).where(Application.Id == application_id)
    ).scalar_one_or_none()


def get_application_detail(db: Session, application_id: int) -> Optional[Application]:
    """Lấy application kèm đầy đủ relationships."""
    return db.execute(
        select(Application)
        .where(Application.Id == application_id)
        .options(
            selectinload(Application.job),
            selectinload(Application.applicant),
            selectinload(Application.cv),
            selectinload(Application.history).selectinload(
                ApplicationHistory.changed_by_user
            ),
        )
    ).scalar_one_or_none()


def get_application_by_job_and_applicant(
    db: Session, job_id: int, applicant_id: int
) -> Optional[Application]:
    """Kiểm tra ứng viên đã nộp vào job này chưa."""
    return db.execute(
        select(Application).where(
            Application.JobId == job_id,
            Application.ApplicantId == applicant_id,
        )
    ).scalar_one_or_none()


def get_applications_by_applicant(
    db: Session,
    applicant_id: int,
    skip: int = 0,
    limit: int = 20,
) -> Tuple[List[Application], int]:
    """Lấy danh sách đơn ứng tuyển của 1 user."""
    query = (
        select(Application)
        .where(Application.ApplicantId == applicant_id)
        .options(selectinload(Application.job))
    )
    total = db.execute(
        select(func.count()).select_from(query.subquery())
    ).scalar_one()

    apps = db.execute(
        query.offset(skip).limit(limit).order_by(Application.AppliedAt.desc())
    ).scalars().all()

    return apps, total


def get_applications_by_job(
    db: Session,
    job_id: int,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
) -> Tuple[List[Application], int]:
    """Lấy danh sách ứng viên theo job (cho HR)."""
    query = (
        select(Application)
        .where(Application.JobId == job_id)
        .options(
            selectinload(Application.applicant),
            selectinload(Application.cv),
        )
    )
    if status:
        query = query.where(Application.Status == status)

    total = db.execute(
        select(func.count()).select_from(query.subquery())
    ).scalar_one()

    apps = db.execute(
        query.offset(skip).limit(limit).order_by(Application.AppliedAt.desc())
    ).scalars().all()

    return apps, total


def create_application(
    db: Session,
    job_id: int,
    cv_id: int,
    applicant_id: int,
    cover_letter: Optional[str] = None,
) -> Application:
    try:
        app = Application(
            JobId=job_id,
            CVId=cv_id,
            ApplicantId=applicant_id,
            CoverLetter=cover_letter,
            Status=ApplicationStatus.APPLIED,
        )
        db.add(app)
        db.flush()
        return app
    except Exception:
        db.rollback()
        raise


def update_application_status(
    db: Session,
    application_id: int,
    new_status: ApplicationStatus,
) -> Application:
    try:
        app = get_application_by_id(db, application_id)
        if not app:
            raise ValueError("Application not found")
        app.Status = new_status
        db.commit()
        db.refresh(app)
        return app
    except ValueError:
        raise
    except Exception:
        db.rollback()
        raise


# ── ApplicationHistory ────────────────────────────────────────────────────────

def create_history_entry(
    db: Session,
    application_id: int,
    status: ApplicationStatus,
    changed_by_id: Optional[int] = None,
    note: Optional[str] = None,
) -> ApplicationHistory:
    try:
        entry = ApplicationHistory(
            ApplicationId=application_id,
            Status=status,
            Note=note,
            ChangedById=changed_by_id,
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
    except Exception:
        db.rollback()
        raise


def get_history_by_application(
    db: Session, application_id: int
) -> List[ApplicationHistory]:
    return db.execute(
        select(ApplicationHistory)
        .where(ApplicationHistory.ApplicationId == application_id)
        .options(selectinload(ApplicationHistory.changed_by_user))
        .order_by(ApplicationHistory.ChangedAt)
    ).scalars().all()