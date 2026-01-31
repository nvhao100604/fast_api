from sqlalchemy import String, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import TYPE_CHECKING, List

class JobEmbedding(Base):
    __tablename__ = "JobEmbeddings"

    Id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    JobId = Column(String(36), ForeignKey("Jobs.Id"))
    ModelName = Column(String(100))
    Vector = Column(Vector(384))
    CreatedAt = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="embeddings")
