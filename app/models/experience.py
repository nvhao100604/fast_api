from sqlalchemy import String, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import TYPE_CHECKING, List

class Experience(Base):
    __tablename__ = "Experiences"

    Id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    CVId = Column(String(36), ForeignKey("CVs.Id"))
    Company = Column(String(200))
    Position = Column(String(200))
    StartDate = Column(Date)
    EndDate = Column(Date)
    DurationMonths = Column(Integer)

    cv = relationship("CV", back_populates="experiences")
