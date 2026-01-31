from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Text, DECIMAL, Date
from app.core.database import Base
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING, List
from sqlalchemy.sql import func

class Job(Base):
    __tablename__ = "Jobs"

    Title = Column(String(200))
    Description = Column(Text)
    RequirementsText = Column(Text)
    MinExperience = Column(DECIMAL)
    EducationLevel = Column(String(100))
    Status = Column(String(50))
    CreatedAt = Column(DateTime, default=func.now())

    embeddings = relationship("JobEmbedding", back_populates="job", cascade="all, delete-orphan")
    match_results = relationship("MatchResult", back_populates="job")
