from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Text, Date
from app.core.database import Base
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING, List
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

class JobEmbedding(Base):
    __tablename__ = "JobEmbeddings"

    JobId = Column(String(36), ForeignKey("Jobs.Id"))
    ModelName = Column(String(100))
    Vector = Column(Vector(384))
    CreatedAt = Column(DateTime, default=func.now())

    job = relationship("Job", back_populates="embeddings")
