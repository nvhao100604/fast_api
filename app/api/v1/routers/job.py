from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_hr_or_admin
from app.services import job_service
from app.core.database import get_db
from app.models.enum import JobStatus
from app.api.v1.schemas.job import JobFilter, JobResponse, JobUpdate

router = APIRouter()

#=═══════════════════════════════════════════════════════
# QUẢN LÝ JOB — HR và Admin quản lý các job
#=═══════════════════════════════════════════════════════

@router.get("/", response_model=list[JobResponse], summary="Xem danh sách tất cả các job")
async def get_all_jobs(
    filters: JobFilter = Depends(),
    db: Session = Depends(get_db),
):
    """Xem danh sách tất cả các job, có thể lọc theo title, requirement text, status."""
    jobs, total = await job_service.get_jobs(db, filters)
    return [JobResponse.model_validate(job) for job in jobs]


@router.get("/{job_id}", response_model=JobResponse, summary="Xem chi tiết một job")
async def get_job_detail(
    job_id: int,
    db: Session = Depends(get_db),
):
    """Xem chi tiết một job theo ID."""
    job = job_service.get_job_detail(db, job_id)

    if not job:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Không tìm thấy job {job_id}"
        )

    return await JobResponse.model_validate(job)


@router.put("/{job_id}", response_model=JobResponse, summary="Cập nhật thông tin của một job")
async def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
    dependencies = [Depends(require_hr_or_admin)]
):
    """Cập nhật thông tin của một job (title, description, requirements_text)."""
    updated_job = job_service.update_job(db, job_id, job_data)
    return await JobResponse.model_validate(updated_job)

@router.post("/", response_model=JobResponse, summary="Tạo một job mới")
async def create_job(
    job_data: JobResponse,
    db: Session = Depends(get_db),
    dependencies = [Depends(require_hr_or_admin)]
):
    """Tạo một job mới với thông tin được cung cấp."""
    new_job = job_service.create_job(db, **job_data.model_dump())
    return await JobResponse.model_validate(new_job)

