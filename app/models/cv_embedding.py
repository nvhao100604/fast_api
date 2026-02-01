from sqlalchemy import String, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import TYPE_CHECKING, List



class CVEmbedding(Base):
    __tablename__ = "CVEmbeddings"

    Id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    CVId = Column(String(36), ForeignKey("CVs.Id"))
    ModelName = Column(String(100))
    Vector = Column(Vector(384))
    CreatedAt = Column(DateTime, default=datetime.utcnow)

    cv = relationship("CV", back_populates="embeddings")
