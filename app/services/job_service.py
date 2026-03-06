from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.crud import job as job_crud
from app.models.job import Job
from app.api.v1.schemas.job import JobCreate, JobUpdate, JobFilter, JobResponse

def get_jobs(db: Session, filters: JobFilter, skip: int = 0, limit: int = 20) -> tuple[list[JobResponse], int]:
    jobs, total = job_crud.get_jobs(
        db=db,
        skip=skip,
        limit=limit,
        title=filters.title,
        requirement=filters.requirement,
        status=filters.status,
    )
    return [JobResponse.model_validate(job) for job in jobs], total

def create_job(db: Session, job_data: JobCreate) -> JobResponse:
    job = job_crud.create_job(db, **job_data.model_dump())
    return JobResponse.model_validate(job)

def update_job(db: Session, job_id: int, job_data: JobUpdate) -> JobResponse:
    job = job_crud.get_job_by_id(db, job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy job {job_id}"
        )

    updated_job = job_crud.update_job(db, job, **job_data.model_dump(exclude_unset=True))

    return JobResponse.model_validate(updated_job)


def get_job_detail(db: Session, job_id: int) -> JobResponse:
    job = job_crud.get_job_by_id(db, job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy job {job_id}"
        )

    return JobResponse.model_validate(job)

