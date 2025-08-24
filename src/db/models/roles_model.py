from __future__ import annotations
from src.db.init_db import Base
from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship, Mapped, mapped_column

if TYPE_CHECKING:
    from src.db.models import User


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    users: Mapped["User"] = relationship("User", back_populates="role")
