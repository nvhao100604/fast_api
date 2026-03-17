from os import path

from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import os


from app.api.v1.schemas.cv import CVFilter
from app.crud import cv as cv_crud
from app.models.enum import CVFileType, UserRole
from app.utils import file_handling as file_utils

UPLOAD_BASE_DIR = "uploads/cvs"

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.crud import cv as cv_crud
from app.models import User

def get_cv_details(db: Session, cv_id: int, current_user: User):
    """
    Lấy thông tin chi tiết CV với logic phân quyền:
    - HR: Được quyền xem mọi CV.
    - Applicant: Chỉ được quyền xem CV của chính mình (UserId trong CV == current_user.Id).
    """
    # 1. Lấy bản ghi CV từ database
    cv_record = cv_crud.get_cv_by_id(db=db, cv_id=cv_id)
    
    if not cv_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Không tìm thấy hồ sơ CV này."
        )

    # 2. Thực hiện kiểm tra quyền (Check Role & Ownership)
    is_hr = (current_user.role == UserRole.HR) 
    is_owner = (cv_record.UserId == current_user.Id) 

    if is_hr or is_owner:
        return cv_record

    # 3. Nếu không phải HR và cũng không phải chủ sở hữu thì chặn truy cập
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Bạn không có quyền truy cập vào hồ sơ CV này."
    )

def upload_and_create_cv(db: Session, file: UploadFile, user_id: int):
    # 1. Validation (Dùng util)
    if not file_utils.check_file_extension(file.filename, ["pdf", "doc", "docx"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF or DOCX files are supported."
        )

    # 2. Xử lý lưu trữ (Dùng util)
    try:
        new_filename = file_utils.generate_unique_filename(user_id, file.filename)
        user_folder = f"{UPLOAD_BASE_DIR}/{user_id}"
        
        saved_path = file_utils.save_file_to_disk(
            file=file, 
            folder_path=user_folder, 
            filename=new_filename
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File storage error: {str(e)}")

    # 3. Mapping enum
    file_type = CVFileType.PDF if file.filename.lower().endswith("pdf") else CVFileType.DOCX

    # 4. DB Record
    return cv_crud.create_cv(
        db=db, 
        applicant_id=user_id, 
        path=saved_path, 
        file_type=file_type
    )

def get_user_cvs(db: Session, current_user: User, filters: CVFilter):
    """
    Service lấy danh sách CV:
    - HR: Xem được tất cả.
    - Applicant: Chỉ xem được của mình.
    """
    filter_dict = filters.model_dump(exclude_none=True)
    
    # Logic phân quyền (RBAC)
    if current_user.role != UserRole.HR:
        # Ép buộc filter theo ID của chính Applicant
        filter_dict["UserId"] = current_user.Id
    
    return cv_crud.get_cvs(db=db, filters=filter_dict)


def get_cv_file_path(db: Session, cv_id: int, current_user: User) -> str:
    """
    Lấy đường dẫn file CV vật lý với logic phân quyền tương tự xem chi tiết:
    - HR: Được quyền tải mọi file CV.
    - Applicant: Chỉ được quyền tải file CV của chính mình.
    """
    # 1. Lấy bản ghi CV từ database
    cv_record = cv_crud.get_cv_by_id(db=db, cv_id=cv_id)
    
    if not cv_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Không tìm thấy hồ sơ CV này."
        )

    # 2. Thực hiện kiểm tra quyền (Check Role & Ownership)
    is_hr = (current_user.role == UserRole.HR) 
    is_owner = (cv_record.UserId == current_user.Id) 

    if not (is_hr or is_owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập hoặc tải file CV này."
        )

    # 3. Kiểm tra sự tồn tại của file vật lý trên server
    if not path.exists(cv_record.FileUrl):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="File vật lý không tồn tại trên hệ thống (Physical file missing)."
        )
        
    return cv_record.FileUrl