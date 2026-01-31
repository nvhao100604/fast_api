from sqlalchemy import String, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import TYPE_CHECKING, List

class MatchResult(Base):
    __tablename__ = "MatchResults"

    Id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    CVId = Column(String(36), ForeignKey("CVs.Id"))
    JobId = Column(String(36), ForeignKey("Jobs.Id"))

    SemanticScore = Column(DECIMAL)
    SkillScore = Column(DECIMAL)
    ExperienceScore = Column(DECIMAL)
    EducationScore = Column(DECIMAL)
    TotalScore = Column(DECIMAL)
    Rank = Column(Integer)
    EvaluatedAt = Column(DateTime, default=datetime.utcnow)

    cv = relationship("CV", back_populates="match_results")
    job = relationship("Job", back_populates="match_results")
