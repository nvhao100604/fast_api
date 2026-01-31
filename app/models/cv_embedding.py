from sqlalchemy import String, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .ordering import Order

class CVEmbedding(Base):
    __tablename__ = "CVEmbeddings"

    Id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    CVId = Column(String(36), ForeignKey("CVs.Id"))
    ModelName = Column(String(100))
    Vector = Column(Vector(384))
    CreatedAt = Column(DateTime, default=datetime.utcnow)

    cv = relationship("CV", back_populates="embeddings")

    __tablename__ = "staff"
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    phoneNumber: Mapped[str] = mapped_column(String(10))
    username: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    status: Mapped[int] = mapped_column(SmallInteger, default=1)
    
    roleID: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role: Mapped["Role"] = relationship(back_populates="staffs")
    orders: Mapped[List["Order"]] = relationship(back_populates="staff")