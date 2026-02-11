from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from app.models.enum import UserStatus

# 1. Schema cơ sở: Chứa các trường công khai chung
class HrBase(BaseModel):
    Email: EmailStr
    FullName: Optional[str] = None
    Status: UserStatus = UserStatus.ACTIVE

# 2. Schema dùng cho Đăng ký (Create): Cần nhận mật khẩu thô từ người dùng
class HrCreate(HrBase):
    Password: str  

# 3. Schema dùng cho Cập nhật (Update): Mọi trường đều là tùy chọn
class HrUpdate(BaseModel):
    Email: Optional[EmailStr] = None
    FullName: Optional[str] = None
    Password: Optional[str] = None
    Status: Optional[UserStatus] = None

# 4. Schema trả về (Response):
class HrResponse(HrBase):
    Id: int 
    CreatedAt: datetime
    UpdatedAt: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)