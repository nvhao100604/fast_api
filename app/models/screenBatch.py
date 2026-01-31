from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship

class ScreeningBatch(Base):
    __tablename__ = "ScreeningBatches"
    JobId = Column(Integer, ForeignKey("Jobs.Id"))
    TriggeredBy = Column(Integer, ForeignKey("Hr.Id"))
    TotalCV = Column(Integer)
    ProcessedCV = Column(Integer)
    Status = Column(String(50))
    CreatedAt = Column(DateTime)

