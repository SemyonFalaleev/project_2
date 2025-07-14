from typing import Optional
from uuid import UUID
from fastapi import Form
from pydantic import BaseModel, EmailStr, SerializationInfo, field_serializer
from datetime import datetime
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.dto.category_dto import CategoryDTOGetMin
    from src.dto.user_dto import UserDTOGetMin

class ArticleBase(BaseModel):
    class Config:
        from_attributes = True

class ArticleDTOCreate(ArticleBase):
    name: str
    description: str
    category_id: Optional[int] = None

    @classmethod
    def as_form(
        cls,
        name: str = Form(),
        description: str = Form(),
        category_id: int = Form()
    ) -> "ArticleDTOCreate":
        return cls(name=name, description=description, category_id=category_id)

class ArticleDTOUpdate(ArticleBase):
    name: Optional[str] = None
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    category_id: Optional[int] = None


class ArticleDTOGetMin(ArticleBase):
    id: int
    name: str
    cover_image_url: str
    created_at: datetime
    updated_at: datetime

class ArticleDTOGet(ArticleBase):
    id: int
    name: str
    description: str
    cover_image_url: str
    updated_at: datetime
    created_at: datetime
    category: "CategoryDTOGetMin"
    user: "UserDTOGetMin"

class ArticleDTOGetAll(ArticleBase):
    count: int
    articles: List[ArticleDTOGetMin]

class ArchivedArticleDTOCreate(ArticleBase):
    id: int
    name: str
    description: str
    cover_image_url: str
    updated_at: datetime
    created_at: datetime
    category_id: int 
    user_id: UUID


from src.dto.category_dto import CategoryDTOGetMin
from src.dto.user_dto import UserDTOGetMin
ArticleDTOGet.model_rebuild(_types_namespace={"CategoryDTOGetMin": CategoryDTOGetMin,
                                              "UserDTOGetMin": UserDTOGetMin})


