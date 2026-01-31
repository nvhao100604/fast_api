from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from sqlalchemy import String, ForeignKey, Column, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from typing import TYPE_CHECKING, List

class CVEmbedding(Base):
    __tablename__ = "CVEmbeddings"

    CVId = Column(String(36), ForeignKey("CVs.Id"))
    ModelName = Column(String(100))
    Vector = Column(Vector(384))
    CreatedAt = Column(DateTime, default=func.now())

    cv = relationship("CV", back_populates="embeddings")