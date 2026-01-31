from sqlalchemy import String, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import TYPE_CHECKING, List

class Education(Base):
    __tablename__ = "Educations"

    Id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    CVId = Column(String(36), ForeignKey("CVs.Id"))
    Degree = Column(String(200))
    Major = Column(String(200))
    School = Column(String(200))
    Level = Column(String(50))
    GraduationYear = Column(Integer)

    cv = relationship("CV", back_populates="educations")
