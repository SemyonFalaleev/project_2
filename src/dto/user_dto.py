from typing import TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel, EmailStr, SecretStr
from datetime import datetime
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import List

if TYPE_CHECKING:
    from src.dto.article_dto import ArticleDTOGetMin


class UserDTOCreate(BaseModel):
    email: EmailStr
    phone_number: PhoneNumber
    name: str
    role_id: int


class UserDTOGet(BaseModel):
    id: UUID
    name: str
    role_id: int
    created_at: datetime
    articles: List["ArticleDTOGetMin"]


class UserDTOGetMin(BaseModel):
    id: UUID
    name: str
    created_at: datetime


class UserSignUpDTO(BaseModel):
    name: str
    email: EmailStr
    phone_number: PhoneNumber
    password: SecretStr


from src.dto.article_dto import ArticleDTOGetMin  # noqa: E402

UserDTOGet.model_rebuild(_types_namespace={"ArticleDTOGetMin": ArticleDTOGetMin})
