from typing import Optional
from uuid import UUID
from src.db.models import User
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic_extra_types.phone_numbers import PhoneNumber

class UserSignInDTO(BaseModel):
    pass

class UserSignUpDTO(BaseModel):
    pass