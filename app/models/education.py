from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Text, Date
from app.core.database import Base
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING, List

class Education(Base):
    __tablename__ = "Educations"

    CVId = Column(String(36), ForeignKey("CVs.Id"))
    Degree = Column(String(200))
    Major = Column(String(200))
    School = Column(String(200))
    Level = Column(String(50))
    GraduationYear = Column(Integer)

    cv = relationship("CV", back_populates="educations")
