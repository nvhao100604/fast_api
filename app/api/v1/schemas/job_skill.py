from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from decimal import Decimal
from .skill import SkillResponse
from .job import JobResponse

# Schema cơ sở chứa các ràng buộc về kỹ năng cho công việc
class JobSkillBase(BaseModel):
    JobId: int
    SkillId: int
    Importance: Optional[Decimal] = Field(default=Decimal("1.0"), max_digits=5, decimal_places=2)
    MinYears: Optional[Decimal] = Field(None, max_digits=3, decimal_places=1)

# Schema dùng để liên kết kỹ năng vào một tin tuyển dụng
class JobSkillCreate(JobSkillBase):
    pass

# Schema dùng để thay đổi yêu cầu hoặc trọng số kỹ năng
class JobSkillUpdate(BaseModel):
    Importance: Optional[Decimal] = None
    MinYears: Optional[Decimal] = None

# Schema trả về dữ liệu kèm theo định danh
class JobSkillResponse(JobSkillBase):
    Id: int 
    # skill: SkillResponse
    # job: JobResponse

    model_config = ConfigDict(from_attributes=True)    