from __future__ import annotations
from typing import List, TYPE_CHECKING
from src.db.init_db import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column

if TYPE_CHECKING:
    from src.db.models import ArchivedArticle, Article


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)

    articles: Mapped[List["Article"]] = relationship(
        "Article", back_populates="category"
    )
    archived_articles: Mapped[List["ArchivedArticle"]] = relationship(
        "ArchivedArticle", back_populates="category"
    )
