from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum

from app.core.database import Base
from app.models.enum import UserStatus

if TYPE_CHECKING:
    from app.models.screenBatch import ScreeningBatch

class Hr(Base):
    __tablename__ = "Hr"
    __table_args__ = (UniqueConstraint("Email", name="uq_hr_email"),)
    
    Email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    PasswordHash: Mapped[str] = mapped_column(String(255))
    FullName: Mapped[Optional[str]] = mapped_column(String(200))
    Status: Mapped[UserStatus] = mapped_column(
        SQLEnum(UserStatus), 
        default=UserStatus.ACTIVE
    )
    
    CreatedAt: Mapped[datetime] = mapped_column(server_default=func.now())
    UpdatedAt: Mapped[Optional[datetime]] = mapped_column(
        server_default=func.now(), 
        onupdate=func.now()
    )

    batches: Mapped[List["ScreeningBatch"]] = relationship(back_populates="hr")




























