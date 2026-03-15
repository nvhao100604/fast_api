from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ── Enums ─────────────────────────────────────────────────────────────────────
class ApplicationStatusEnum(str, Enum):
    APPLIED = "APPLIED"
    SHORTLISTED = "SHORTLISTED"
    INTERVIEW = "INTERVIEW"
    REJECTED = "REJECTED"
    HIRED = "HIRED"


# ── Application schemas ───────────────────────────────────────────────────────
class ApplicationCreate(BaseModel):
    job_id: int
    cv_id: int
    cover_letter: Optional[str] = None


class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatusEnum
    note: Optional[str] = Field(default=None, max_length=1000)


class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    job_title: Optional[str] = None
    cv_id: int
    applicant_id: int
    applicant_name: Optional[str] = None
    status: ApplicationStatusEnum
    cover_letter: Optional[str] = None
    applied_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ApplicationHistoryResponse(BaseModel):
    id: int
    status: ApplicationStatusEnum
    note: Optional[str] = None
    changed_at: datetime
    changed_by: Optional[str] = None

    model_config = {"from_attributes": True}


class ApplicationDetailResponse(ApplicationResponse):
    history: List[ApplicationHistoryResponse] = []
