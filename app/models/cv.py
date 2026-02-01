from sqlalchemy import String, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING, List



class CV(Base):
    __tablename__ = "CVs"

    Id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    CandidateId = Column(String(36), ForeignKey("Candidates.Id"))
    FileUrl = Column(String(500))
    FileType = Column(String(20))
    RawText = Column(Text)
    CleanText = Column(Text)
    Summary = Column(Text)
    Language = Column(String(20))
    CreatedAt = Column(DateTime, default=datetime.utcnow)

    embeddings = relationship("CVEmbedding", back_populates="cv", cascade="all, delete-orphan")
    experiences = relationship("Experience", back_populates="cv", cascade="all, delete-orphan")
    educations = relationship("Education", back_populates="cv", cascade="all, delete-orphan")
    skills = relationship("CVSkill", back_populates="cv", cascade="all, delete-orphan")
    match_results = relationship("MatchResult", back_populates="cv")


# class Staff(Base):
#     __tablename__ = "staff"
#     name: Mapped[str] = mapped_column(String(255))
#     email: Mapped[str] = mapped_column(String(255))
#     phoneNumber: Mapped[str] = mapped_column(String(10))
#     username: Mapped[str] = mapped_column(String(255))
#     password: Mapped[str] = mapped_column(String(255))
#     status: Mapped[int] = mapped_column(SmallInteger, default=1)
    
#     roleID: Mapped[int] = mapped_column(ForeignKey("roles.id"))
#     role: Mapped["Role"] = relationship(back_populates="staffs")
#     orders: Mapped[List["Order"]] = relationship(back_populates="staff")