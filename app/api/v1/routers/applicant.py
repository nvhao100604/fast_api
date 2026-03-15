from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.orm import Session

# imports thêm vào đầu file
from app import utils
from app.api.v1.schemas.cv import CVUploadResponse
from app.api.v1.schemas.education import EducationCreate
from app.api.v1.schemas.experience import ExperienceCreate
from app.api.v1.schemas.skill import CVSkillCreate
from app.services import education as edu_service
from app.services import experience as exp_service
from app.services import skill as skill_service
from app.crud import cv as cv_crud
from app.api.deps import get_db, get_current_user, require_applicant, require_hr
from app.api.v1.schemas import ResponseSchema, PersonalInfoResponse
from app.api.v1.schemas.cv import CVResponse, PersonalInfoUpdate
from app.models import User
from app.services import applicant as applicant_service

router = APIRouter()
applicant_router = APIRouter(dependencies=[Depends(require_applicant)])
hr_router = APIRouter(dependencies=[Depends(require_hr)])


# --- APPLICANT --- (chỉ chính chủ)

@applicant_router.post(
    "/me/cv/upload",
    response_model=ResponseSchema[CVUploadResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Upload & Parse CV",
    description="Upload file CV, tự động trích xuất và lưu thông tin học vấn, kinh nghiệm, kỹ năng."
)
async def upload_and_parse_cv(
    cv_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Lưu file và lấy URL
    file_url = await utils.save_file_to_disk(file, current_user.Id)

    # 2. Parse file → trích xuất dữ liệu
    parsed = await utils.parse_cv_file(file)
    # parsed = {
    #     "educations": [...],
    #     "experiences": [...],
    #     "skills": [...]
    # }

    # 3. Insert Education
    for edu_data in parsed.get("educations", []):
        edu_in = EducationCreate(**edu_data, CVId=cv_id)
        edu_service.add_education(db, current_user.Id, edu_in)

    # 4. Insert Experience
    for exp_data in parsed.get("experiences", []):
        exp_in = ExperienceCreate(**exp_data, CVId=cv_id)
        exp_service.add_experience(db, current_user.Id, exp_in)

    # 5. Insert Skill
    for skill_data in parsed.get("skills", []):
        skill_in = CVSkillCreate(**skill_data, CVId=cv_id)
        skill_service.add_skill_to_cv(db, current_user, skill_in)

    # 6. Lưu metadata CV + file_url vào DB
    cv = cv_crud.create_cv(
        db,
        applicant_id=current_user.Id,
        path=file_url,
        file_type=file.content_type
    )

    return ResponseSchema[CVUploadResponse](
        success=True,
        message="CV uploaded and parsed successfully",
        data=CVUploadResponse(file_url=file_url, cv_id=cv.Id)
    )

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