from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy import select, and_, or_
# from src.dto.user_dto import UserSignInDTO
from src.dto.validation_func import validate_email, validate_phone
from src.db.init_db import AsyncSession, get_async_db
from src.db.models import User
from sqlalchemy.exc import IntegrityError
from src.tools.hashed_func import Hasher
from fastapi.security import OAuth2PasswordRequestForm
from src.tools.security import create_access_token

router = APIRouter()


@router.post("/logout")
async def logout_user():
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie(key="access_token", path='/')
    return response