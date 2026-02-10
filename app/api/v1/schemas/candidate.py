from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from typing import List, Optional
from .cv import CVResponse

# Schema cơ sở chứa các trường chung
class CandidateBase(BaseModel):
    FullName: str
    Email: Optional[EmailStr] = None
    Phone: Optional[str] = None
    Location: Optional[str] = None

    @field_validator("Phone")
    @classmethod
    def validate_phone(cls, v: str):
        if v is None: return v
        v = v.strip()
        if not v.startswith("0"):
            raise ValueError("Invalid phone number. The first digit must be '0'.")
        if len(v) != 10:
            raise ValueError(f"Phone number must be exactly 10 digit long (currently {len(v)}).")
        
        if not v.isdigit():
            raise ValueError("Phone number must contain only numeric characters from (0-9).")
            
        return v

# Schema dùng cho thao tác Tạo mới (Create)
class CandidateCreate(CandidateBase):
    pass

# Schema dùng cho thao tác Cập nhật (Update) - mọi trường đều là Optional
class CandidateUpdate(BaseModel):
    FullName: Optional[str] = None
    Email: Optional[EmailStr] = None
    Phone: Optional[str] = None
    Location: Optional[str] = None

# Schema dùng để trả về dữ liệu (Response/Read)
class CandidateResponse(CandidateBase):
    Id: int
    # cvs: List[CVResponse] = [] 

    model_config = ConfigDict(from_attributes=True)

class CandidateFilter(CandidateUpdate):
    pass