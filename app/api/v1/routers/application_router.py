from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, require_applicant, require_hr, require_hr_or_admin
from app.models.User import User, UserRole
from app.api.v1.schemas.application_schemas import (
    ApplicationCreate,
    ApplicationStatusUpdate,
    ApplicationResponse,
    ApplicationDetailResponse,
    ApplicationHistoryResponse,
)
from app.services.application_service import ApplicationService

router = APIRouter()


# ─────────────────────────────────────────────────────────────────────────────
# Nộp đơn ứng tuyển (Applicant)
# ─────────────────────────────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=ApplicationDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Nộp CV vào vị trí tuyển dụng",
    dependencies=[Depends(require_applicant)]
)
def apply_for_job(
    data: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ApplicationDetailResponse.model_validate(
        ApplicationService.apply(db, data, applicant_id=current_user.Id)
    )


# ─────────────────────────────────────────────────────────────────────────────
# Lịch sử ứng tuyển của tôi (Applicant)
# ─────────────────────────────────────────────────────────────────────────────
@router.get(
    "/me",
    response_model=dict,
    summary="Lịch sử ứng tuyển của tôi",
    dependencies=[Depends(require_applicant)]
)
def my_applications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    apps, total = ApplicationService.get_my_applications(
        db, applicant_id=current_user.Id, skip=skip, limit=limit
    )
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": [ApplicationResponse.model_validate(a) for a in apps],
    }


# ─────────────────────────────────────────────────────────────────────────────
# Chi tiết đơn ứng tuyển
# ─────────────────────────────────────────────────────────────────────────────
@router.get(
    "/{application_id}",
    response_model=ApplicationDetailResponse,
    summary="Chi tiết đơn ứng tuyển"
)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    app = ApplicationService.get_application(db, application_id)
    # Ứng viên chỉ xem được đơn của mình; HR/Admin xem được tất cả
    if (
        current_user.role == UserRole.APPLICANT
        and app.ApplicantId != current_user.Id
    ):
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Không có quyền truy cập")
    return app


# ─────────────────────────────────────────────────────────────────────────────
# Cập nhật trạng thái (HR)
# ─────────────────────────────────────────────────────────────────────────────
@router.patch(
    "/{application_id}/status",
    response_model=ApplicationDetailResponse,
    summary="Cập nhật trạng thái ứng viên (Applied → Shortlisted → Interview → Rejected/Hired)",
    dependencies=[Depends(require_hr)]
)
def update_application_status(
    application_id: int,
    data: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ApplicationService.update_status(
        db, application_id, data, changed_by_id=current_user.Id
    )


# ─────────────────────────────────────────────────────────────────────────────
# Lịch sử trạng thái của đơn
# ─────────────────────────────────────────────────────────────────────────────
@router.get(
    "/{application_id}/history",
    response_model=list[ApplicationHistoryResponse],
    summary="Lịch sử thay đổi trạng thái",
)
def get_application_history(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ApplicationService.get_history(db, application_id)

