from sqlalchemy import Column, String
from app.core.database import Base
from sqlalchemy.orm import relationship

class Candidate(Base):
    __tablename__ = "Candidates"
    FullName = Column(String(200))
    Email = Column(String(255))
    Phone = Column(String(50))
    Location = Column(String(200))

