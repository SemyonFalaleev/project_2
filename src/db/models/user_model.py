from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from src.db.init_db import Base
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    UUID,
    func,
    ForeignKey,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
import uuid

if TYPE_CHECKING:
    from src.db.models import Article, ArchivedArticle, Role


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    phone_number: Mapped[str] = mapped_column(
        String(length=30), nullable=False, unique=True
    )
    email: Mapped[str] = mapped_column(String(length=254), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    hashed_password: Mapped[str] = mapped_column(String(length=300), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    activated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    articles: Mapped[List["Article"]] = relationship("Article", back_populates="user")
    archived_articles: Mapped[List["ArchivedArticle"]] = relationship(
        "ArchivedArticle", back_populates="user"
    )
    role: Mapped["Role"] = relationship("Role", back_populates="users")
