from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, DECIMAL
from app.core.database import Base
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING, List
from sqlalchemy.sql import func

class MatchResult(Base):
    __tablename__ = "MatchResults"

    CVId = Column(String(36), ForeignKey("CVs.Id"))
    JobId = Column(String(36), ForeignKey("Jobs.Id"))

    SemanticScore = Column(DECIMAL)
    SkillScore = Column(DECIMAL)
    ExperienceScore = Column(DECIMAL)
    EducationScore = Column(DECIMAL)
    TotalScore = Column(DECIMAL)
    Rank = Column(Integer)
    EvaluatedAt = Column(DateTime, default=func.now())

    cv = relationship("CV", back_populates="match_results")
    job = relationship("Job", back_populates="match_results")
