from typing import List, Dict, Any

from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, require_applicant, require_hr
from app.api.v1.schemas import ResponseSchema
from app.api.v1.schemas.application_schemas import (
    ApplicationCreate,
    ApplicationStatusUpdate,
    ApplicationResponse,
    ApplicationDetailResponse,
    ApplicationHistoryResponse,
)
from app.models import User
from app.services.application_service import ApplicationService

router = APIRouter()
applicant_router = APIRouter(dependencies=[Depends(require_applicant)])
hr_router = APIRouter(dependencies=[Depends(require_hr)])

# ─────────────────────────────────────────────────────────────────────────────
# APPLICANT ROUTER (Dành cho ứng viên)
# ─────────────────────────────────────────────────────────────────────────────

@applicant_router.post(
    "/me/apply",
    response_model=ResponseSchema[ApplicationDetailResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Apply for Job",
    description="Ứng viên nộp hồ sơ vào một vị trí tuyển dụng nhất định."
)
def create_application(
    data: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Service sẽ xử lý logic tạo đơn và kiểm tra xem vị trí job có tồn tại không
    result = ApplicationService.apply(db, data, applicant_id=current_user.Id)
    return ResponseSchema[ApplicationDetailResponse](
        success=True,
        message="Application submitted successfully",
        data=result
    )


@applicant_router.get(
    "/me/applications",
    response_model=ResponseSchema[Dict[str, Any]],
    summary="Get My Applications",
    description="Xem danh sách các đơn đã nộp của chính người dùng hiện tại."
)
def get_my_applications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    apps, total = ApplicationService.get_my_applications(
        db, applicant_id=current_user.Id, skip=skip, limit=limit
    )
    
    data = {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": [ApplicationResponse.model_validate(a) for a in apps],
    }
    
    return ResponseSchema[Dict[str, Any]](
        success=True,
        message="Fetched your applications successfully",
        data=data
    )


# ─────────────────────────────────────────────────────────────────────────────
# HR ROUTER (Dành cho nhân sự/quản lý)
# ─────────────────────────────────────────────────────────────────────────────

@hr_router.patch(
    "/{application_id}/status",
    response_model=ResponseSchema[ApplicationDetailResponse],
    summary="Update Application Status",
    description="HR cập nhật trạng thái đơn (Applied -> Shortlisted -> Interview -> Rejected/Hired)."
)
def update_status(
    application_id: int,
    data: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = ApplicationService.update_status(
        db, application_id, data, changed_by_id=current_user.Id
    )
    return ResponseSchema[ApplicationDetailResponse](
        success=True,
        message=f"Application status updated to {data.status}",
        data=result
    )


# ─────────────────────────────────────────────────────────────────────────────
# GENERAL ROUTER (Dành cho cả Applicant và HR - Xử lý phân quyền trong Service)
# ─────────────────────────────────────────────────────────────────────────────

@router.get(
    "/{application_id}",
    response_model=ResponseSchema[ApplicationDetailResponse],
    summary="Get Application Detail",
    description="Xem chi tiết đơn ứng tuyển. Ứng viên chỉ xem được đơn của mình, HR xem được tất cả."
)
def get_application_detail(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Đẩy logic kiểm tra quyền (if current_user.Id != app.ApplicantId) vào Service
    data = ApplicationService.get_application_detail_with_auth(db, application_id, current_user)
    
    return ResponseSchema[ApplicationDetailResponse](
        success=True,
        message="Fetched application detail successfully",
        data=data
    )


@router.get(
    "/{application_id}/history",
    response_model=ResponseSchema[List[ApplicationHistoryResponse]],
    summary="Get Status History",
    description="Xem lịch sử thay đổi trạng thái của một đơn ứng tuyển."
)
def get_application_history(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Kiểm tra quyền xem lịch sử trong Service
    data = ApplicationService.get_history(db, application_id, current_user)
    
    return ResponseSchema[List[ApplicationHistoryResponse]](
        success=True,
        message="Fetched application history successfully",
        data=data
    )


# ─────────────────────────────────────────────────────────────────────────────
# INCLUDE ROUTERS
# ─────────────────────────────────────────────────────────────────────────────

router.include_router(applicant_router)
router.include_router(hr_router)