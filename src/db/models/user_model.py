from src.db.init_db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, UUID, func, ForeignKey
import uuid
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    phone_number = Column(String(length=30), nullable=False, unique=True)
    email = Column(String(length=254), nullable=False, unique=True)
    name = Column(String(length=100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    role_id = Column(Integer, ForeignKey("roles.id"))
    hashed_password = Column(String(length=300), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    activated_at = Column(DateTime(timezone=True), nullable=True)

    articles = relationship("Article", back_populates="user")
    archived_articles = relationship("ArchivedArticle", back_populates="user")
    role = relationship("Role", back_populates="users")

