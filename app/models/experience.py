from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Text, Date
from app.core.database import Base
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING, List

class Experience(Base):
    __tablename__ = "Experiences"

    CVId = Column(String(36), ForeignKey("CVs.Id"))
    Company = Column(String(200))
    Position = Column(String(200))
    StartDate = Column(Date)
    EndDate = Column(Date)
    DurationMonths = Column(Integer)

    cv = relationship("CV", back_populates="experiences")
