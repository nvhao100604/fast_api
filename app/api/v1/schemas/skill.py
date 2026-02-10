from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class SkillBase(BaseModel):
    Name: str = Field(..., max_length=200)
    Description: Optional[str] = Field(None, max_length=500)
    Category: Optional[str] = Field(None, max_length=100)

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    Name: Optional[str] = None
    Description: Optional[str] = None
    Category: Optional[str] = None

class SkillResponse(SkillBase):
    Id: int
    
    model_config = ConfigDict(from_attributes=True)