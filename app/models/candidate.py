from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.cv import CV
    
class Candidate(Base):
    __tablename__ = "Candidates"

    FullName: Mapped[str] = mapped_column(String(200), index=True)
    Email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True)
    Phone: Mapped[Optional[str]] = mapped_column(String(50))
    Location: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Cascade giúp khi xóa Candidate thì tự động xóa hết CV của họ
    cvs: Mapped[List["CV"]] = relationship(back_populates="candidate", cascade="all, delete-orphan")