from typing import Optional
from uuid import UUID
from fastapi import Form
from pydantic import BaseModel, field_serializer
from datetime import datetime
from typing import TYPE_CHECKING, List
from decouple import config

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
    @classmethod
    def as_form(
        cls,
        name: str = Form(default=None),
        description: str = Form(default=None),
        category_id: int = Form(default=None)
    ) -> "ArticleDTOCreate":
        return cls(name=name, description=description, category_id=category_id)

class ArticleDTOGetMin(ArticleBase):
    id: int
    name: str
    cover_image_url: str
    created_at: datetime
    updated_at: datetime
    @field_serializer("cover_image_url")
    def serialize_cover_image_url(self, value, info):
        return config("EXTERNAL_HOST_AWS")+value

class ArticleDTOGet(ArticleBase):
    id: int
    name: str
    description: str
    cover_image_url: str
    updated_at: datetime
    created_at: datetime
    category: "CategoryDTOGetMin"
    user: "UserDTOGetMin"
    @field_serializer("cover_image_url")
    def serialize_cover_image_url(self, value, info):
        return config("EXTERNAL_HOST_AWS")+value

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


