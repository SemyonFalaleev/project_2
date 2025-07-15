from typing import List
from jose import jwt
from datetime import datetime, timedelta
from decouple import config
import json

USER_ROLE = 1
AUTHOR_ROLE = 2
ADMIN_ROLE = 3

UNPROTECTED_ROUTES: List[str] = ["/docs", "/openapi.json", "/", "/auth/"]


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    payload = {
        "sub": str(data.get("id")),
        "id": data.get("id"),
        "role_id": data.get("role_id"),
    }

    expire = datetime.now() + (
        expires_delta or timedelta(minutes=int(config("TOKEN_EXPIRE")))
    )
    payload.update({"exp": expire})
    return jwt.encode(
        payload, config("SECRET_KEY_JWT"), algorithm=config("ALGORITM_JWT")
    )


def create_email_token(data: dict, expires_delta: timedelta = None) -> str:
    payload = {"sub": str(data.get("id")), "id": data.get("id")}

    expire = datetime.now() + (
        expires_delta or timedelta(minutes=int(config("TOKEN_EMAIL_EXPIRE")))
    )
    payload.update({"exp": expire})
    return jwt.encode(
        payload, config("SECRET_KEY_JWT"), algorithm=config("ALGORITM_JWT")
    )


def parse_permission_dict(path: str):
    with open(path, "r") as file:
        permission = json.load(file)

    return permission


def match_path(actual_path: str, pattern_path: str) -> bool:
    if "{*}" not in pattern_path:
        return actual_path.startswith(pattern_path)
    prefix = pattern_path.split("{*}")[0]
    return actual_path.startswith(prefix)
