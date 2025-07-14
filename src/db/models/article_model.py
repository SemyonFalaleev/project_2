from src.db.init_db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, UUID, func, ForeignKey
from sqlalchemy.orm import relationship

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    cover_image_url = Column(String, nullable=False) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now())
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="articles")
    category = relationship("Category", back_populates="articles")

class ArchivedArticle(Base):
    __tablename__ = "archived_articles"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    cover_image_url = Column(String, nullable=False) 
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    deleted_at = Column(DateTime(timezone=(True)), default=func.now())
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="archived_articles") 
    category = relationship("Category", back_populates="archived_articles")