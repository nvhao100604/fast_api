from sqlalchemy import String, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import TYPE_CHECKING, List

class Job(Base):
    __tablename__ = "Jobs"

    Id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    Title = Column(String(200))
    Description = Column(Text)
    RequirementsText = Column(Text)
    MinExperience = Column(DECIMAL)
    EducationLevel = Column(String(100))
    Status = Column(String(50))
    CreatedAt = Column(DateTime, default=datetime.utcnow)

    embeddings = relationship("JobEmbedding", back_populates="job", cascade="all, delete-orphan")
    match_results = relationship("MatchResult", back_populates="job")
