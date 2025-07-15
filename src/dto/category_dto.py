from typing import Optional
from pydantic import BaseModel
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.dto.article_dto import ArticleDTOGetMin


class CategoryBase(BaseModel):
    class Config:
        from_attributes = True


class CategoryDTOCreate(CategoryBase):
    name: str
    description: str


class CategoryDTOGetMin(CategoryBase):
    id: int
    name: str
    description: str


class CategoryDTOGet(CategoryBase):
    id: int
    name: str
    description: str
    articles: List["ArticleDTOGetMin"]


class CategoryDTOUpdate(CategoryBase):
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryDTOGetAll(CategoryBase):
    count: int
    categories: List[CategoryDTOGetMin]


from src.dto.article_dto import ArticleDTOGetMin  # noqa: E402

CategoryDTOGet.model_rebuild(_types_namespace={"ArticleDTOGetMin": ArticleDTOGetMin})
