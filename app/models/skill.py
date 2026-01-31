from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Text, Decimal, Date
from app.core.database import Base
from sqlalchemy.orm import relationship

class Skill (Base):
    __tablename__ = "Skills"
    Name = Column(String (200))
    Category = Column(String (100))
