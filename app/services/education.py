from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.schemas.education import EducationCreate, EducationUpdate
from app.crud import education as edu_crud


def add_education(db: Session, user_id: int, edu_in: EducationCreate):
    """Thêm mới học vấn."""
    return edu_crud.create_education(
        db, edu_in.CVId, user_id,
        edu_in.model_dump(exclude={"CVId"})
    )


def patch_education_service(db: Session, edu_id: int, cv_id: int, user_id: int, edu_in: EducationUpdate):
    """Cập nhật từng phần học vấn."""
    update_data = edu_in.model_dump(exclude_none=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không có dữ liệu thay đổi."
        )

    data = edu_crud.update_education(db, edu_id, cv_id, user_id, update_data)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy bản ghi học vấn hoặc bạn không có quyền sở hữu."
        )
    return data


def delete_education_service(db: Session, edu_id: int, cv_id: int, user_id: int) -> bool:
    """Xóa học vấn."""
    success = edu_crud.delete_education(db, edu_id, cv_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy học vấn."
        )
    return success