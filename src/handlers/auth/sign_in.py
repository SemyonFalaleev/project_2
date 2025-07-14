from fastapi import APIRouter, Depends, HTTPException, status
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


@router.post(
    "/sign_in",
    status_code=status.HTTP_202_ACCEPTED,
)
async def sign_in_user(data: OAuth2PasswordRequestForm = Depends(), 
                       session: AsyncSession = Depends(get_async_db)):
    try:
        if email:=validate_email(data.username):
            query = await session.execute(select(User).where(User.email == email, 
                                                             User.is_active == True))
        elif phone_number:=validate_phone(data.username):
            query = await session.execute(select(User).where(User.phone_number == phone_number,
                                                             User.is_active == True))
        else: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Please enter a valid email or phone number")
        
        result = query.scalar_one_or_none()
        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User with such data not found")
        if Hasher.verify_password(data.password, result.hashed_password):
            access_token = create_access_token(data={
                "id": str(result.id),
                "role_id": result.role_id
            })
            response = Response(content=("Login successful"),
                                status_code=status.HTTP_200_OK)
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,        
                secure=False,          
                samesite="lax",      
                max_age=60*10)
            return response
        
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="WRONG PASSWORD")
        
    except IntegrityError:
        raise HTTPException(detail="A user with such data already exists",
                            status_code=status.HTTP_400_BAD_REQUEST)
    