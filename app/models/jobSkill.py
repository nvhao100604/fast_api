from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Text, Decimal, Date
from app.core.database import Base
from sqlalchemy.orm import relationship

class JobSkill:
    __tablename__ = "JobSkill"
    JobId = Column(Integer, ForeignKey("Jobs.Id"))
    SkillId = Column(Integer, ForeignKey("Skills.Id"))
    weight = Column(Decimal)