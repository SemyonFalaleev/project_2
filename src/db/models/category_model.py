from src.db.init_db import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)

    articles = relationship("Article", back_populates="category")
    archived_articles = relationship("ArchivedArticle", back_populates="category")
