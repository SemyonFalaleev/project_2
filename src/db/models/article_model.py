from __future__ import annotations

from typing import TYPE_CHECKING
from src.db.init_db import Base
from sqlalchemy import (
    String,
    DateTime,
    UUID,
    func,
    ForeignKey,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

if TYPE_CHECKING:
    from src.db.models import User, Category


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    cover_image_url: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="articles")
    category: Mapped["Category"] = relationship("Category", back_populates="articles")


class ArchivedArticle(Base):
    __tablename__ = "archived_articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    cover_image_url: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    deleted_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="archived_articles")
    category: Mapped["Category"] = relationship(
        "Category", back_populates="archived_articles"
    )
