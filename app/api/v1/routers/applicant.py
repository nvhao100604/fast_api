from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, require_applicant, require_hr
from app.api.v1.schemas import ResponseSchema, PersonalInfoResponse
from app.api.v1.schemas.cv import CVResponse, PersonalInfoUpdate
from app.models import User
from app.services import applicant as applicant_service

router = APIRouter()
applicant_router = APIRouter(dependencies=[Depends(require_applicant)])
hr_router = APIRouter(dependencies=[Depends(require_hr)])


# --- APPLICANT --- (chỉ chính chủ)

@applicant_router.get(
    "/me/profile/{cv_id}",
    response_model=ResponseSchema[PersonalInfoResponse],
    summary="Get My Profile",
    description="Ứng viên tự xem thông tin cá nhân trong hồ sơ CV của mình."
)
def get_my_profile(
    cv_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data = applicant_service.get_applicant_profile(db, cv_id, current_user)
    return ResponseSchema[PersonalInfoResponse](
        success=True,
        message="Fetched profile successfully",
        data=data
    )


@applicant_router.patch(
    "/me/profile/{cv_id}",
    response_model=ResponseSchema[PersonalInfoResponse],
    summary="Update Personal Info",
    description="Cập nhật thông tin tóm tắt (Summary) và ngôn ngữ hồ sơ."
)
def update_my_profile(
    cv_id: int,
    info: PersonalInfoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data = applicant_service.update_personal_info(db, cv_id, current_user, info)
    return ResponseSchema[PersonalInfoResponse](
        success=True,
        message="Profile updated successfully",
        data=data
    )


# --- HR --- (xem hồ sơ người khác)

@hr_router.get(
    "/{applicant_id}/profile/{cv_id}",
    response_model=ResponseSchema[PersonalInfoResponse],
    summary="View Applicant Profile",
    description="HR xem hồ sơ chi tiết của ứng viên bất kỳ."
)
def get_profile(
    applicant_id: int,
    cv_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data = applicant_service.get_applicant_profile(db, cv_id, current_user, applicant_id)
    return ResponseSchema[PersonalInfoResponse](
        success=True,
        message="Fetched applicant profile successfully",
        data=data
    )

@hr_router.get(
    "/{applicant_id}/cvs",
    response_model=ResponseSchema[List[CVResponse]],
    summary="Get Applicant CV List",
    description="HR xem danh sách CV của một ứng viên."
)
def get_applicant_cv_list(
    applicant_id: int,
    db: Session = Depends(get_db),
):
    data = applicant_service.get_cv_list_service(db, applicant_id)
    return ResponseSchema[List[CVResponse]](
        success=True,
        message="Fetched CV list successfully",
        data=data
    )

# --- INCLUDE ---

router.include_router(applicant_router)
router.include_router(hr_router)