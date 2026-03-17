from sqlalchemy.orm import Session
from app.models.cv import CV
from app.models.education import Education

def create_education(db: Session, cv_id: int, user_id: int, edu_in: dict):
    """Thêm mới học vấn - Ràng buộc chặt chẽ với cv_id và user_id."""
    cv_exists = db.query(CV).filter(CV.Id == cv_id, CV.UserId == user_id).first()
    if not cv_exists:
        return None
    
    db_edu = Education(**edu_in, cv_id=cv_id)
    db.add(db_edu)
    db.commit()
    db.refresh(db_edu)
    return db_edu

def update_education(db: Session, edu_id: int, cv_id: int, user_id: int, edu_in: dict):
    """Cập nhật học vấn - Xác thực quyền sở hữu chéo qua join CV."""
    db_edu = db.query(Education).join(CV).filter(
        Education.Id == edu_id, 
        CV.Id == cv_id, 
        CV.UserId == user_id
    ).first()
    
    if db_edu:
        for key, value in edu_in.items():
            setattr(db_edu, key, value)
        db.commit()
        db.refresh(db_edu)
    return db_edu

def delete_education(db: Session, edu_id: int, cv_id: int, user_id: int):
    """Xóa học vấn - Đảm bảo tính an toàn dữ liệu."""
    db_edu = db.query(Education).join(CV).filter(
        Education.Id == edu_id, 
        CV.Id == cv_id, 
        CV.UserId == user_id
    ).first()
    if db_edu:
        db.delete(db_edu)
        db.commit()
        return True
    return False