from pydantic import EmailStr, ValidationError, TypeAdapter
from pydantic_extra_types.phone_numbers import PhoneNumber


def validate_phone(username: str) -> bool | str:
    phone_adapter = TypeAdapter(PhoneNumber)
    phone = False
    try:
        phone = phone_adapter.validate_python(username)
    except ValidationError:
        pass
    return phone


def validate_email(username: str) -> bool | str:
    email_adapter = TypeAdapter(EmailStr)
    email = False
    try:
        email = email_adapter.validate_python(username)
    except ValidationError:
        pass
    return email
