from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Text, Date
from app.core.database import Base
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING, List
from sqlalchemy.sql import func

# if TYPE_CHECKING:
#     from .ordering import Order

class CV(Base):
    __tablename__ = "CVs"

    CandidateId = Column(String(36), ForeignKey("Candidates.Id"))
    FileUrl = Column(String(500))
    FileType = Column(String(20))
    RawText = Column(Text)
    CleanText = Column(Text)
    Summary = Column(Text)
    Language = Column(String(20))
    CreatedAt = Column(DateTime, default=func.now())

    embeddings = relationship("CVEmbedding", back_populates="cv", cascade="all, delete-orphan")
    experiences = relationship("Experience", back_populates="cv", cascade="all, delete-orphan")
    educations = relationship("Education", back_populates="cv", cascade="all, delete-orphan")
    skills = relationship("CVSkill", back_populates="cv", cascade="all, delete-orphan")
    match_results = relationship("MatchResult", back_populates="cv")