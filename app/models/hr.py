from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Text, Decimal, Date
from app.core.database import Base
from sqlalchemy.orm import relationship

class Hr(Base):
    __tablename__ = "Hr"
    Email = Column(String(255), unique=True)
    PasswordHash = Column(String(255))
    FullName = Column(String(200))
    Status = Column(String(50))
    CreatedAt = Column(DateTime)
    UpdatedAt = Column(DateTime)