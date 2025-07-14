from typing import TYPE_CHECKING, Optional, Literal
from uuid import UUID
from src.db.models import User
from pydantic import BaseModel, EmailStr, SecretStr, ValidationError, model_validator, TypeAdapter
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
    id : UUID
    name: str
    role_id: int
    created_at: datetime
    articles: List["ArticleDTOGetMin"]

class UserDTOGetMin(BaseModel):
    id : UUID
    name: str
    created_at: datetime

class UserDTOUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[PhoneNumber] = None

class UserSignInDTO(BaseModel):
    email_or_phone: str
    password: SecretStr  

class UserSignInDTO(BaseModel):
    email_or_phone: str
    password: SecretStr
    login_type: Optional[Literal["email", "phone_number", None]] = None

    @model_validator(mode="before")
    @classmethod
    def validate_email_or_phone(cls, values):
        raw = values.get("email_or_phone")
        if not raw:
            raise ValueError("email or phone number is required")

        email_adapter = TypeAdapter(EmailStr)
        phone_adapter = TypeAdapter(PhoneNumber)

        try:
            email = email_adapter.validate_python(raw)
            values["email_or_phone"] = email
            values["login_type"] = "email"
            return values
        except ValidationError:
            pass

        try:
            phone = phone_adapter.validate_python(raw)
            values["email_or_phone"] = phone
            values["login_type"] = "phone_number"
            return values
        except ValidationError:
            pass

        raise ValueError("email_or_phone must be a valid email or phone number")

class UserSignUpDTO(BaseModel):
    name: str
    email: EmailStr
    phone_number: PhoneNumber
    password: SecretStr 

from src.dto.article_dto import ArticleDTOGetMin 
UserDTOGet.model_rebuild(_types_namespace={"ArticleDTOGetMin": ArticleDTOGetMin})
                                              
