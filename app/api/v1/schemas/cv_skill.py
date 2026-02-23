from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from decimal import Decimal

from app.api.v1.schemas.cv import CVResponse
from app.api.v1.schemas.skill import SkillResponse

class CVSkillBase(BaseModel):
    CVId: int
    SkillId: int
    Confidence: Optional[Decimal] = Field(None, max_digits=5, decimal_places=2)
    Source: Optional[str] = Field(None, max_length=100)

class CVSkillCreate(CVSkillBase):
    pass

class CVSkillUpdate(BaseModel):
    Confidence: Optional[Decimal] = None
    Source: Optional[str] = None

class CVSkillResponse(CVSkillBase):
    Id: int 
    # cv: CVResponse
    # skill: SkillResponse
    
    model_config = ConfigDict(from_attributes=True)