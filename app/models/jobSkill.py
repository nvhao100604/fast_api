from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from app.core.database import Base
from sqlalchemy.orm import relationship

class JobSkill(Base):
    __tablename__ = "JobSkill"
    JobId = Column(Integer, ForeignKey("Jobs.Id"))
    SkillId = Column(Integer, ForeignKey("Skills.Id"))
    weight = Column(DECIMAL)