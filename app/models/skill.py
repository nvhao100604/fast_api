from sqlalchemy import Column, String
from app.core.database import Base
from sqlalchemy.orm import relationship

class Skill (Base):
    __tablename__ = "Skills"
    Name = Column(String (200))
    Category = Column(String (100))
