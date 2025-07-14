from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy import select
from src.dto.user_dto import UserSignUpDTO, UserDTOGet
from src.db.init_db import AsyncSession, get_async_db
from src.db.models import User
from sqlalchemy.exc import IntegrityError
from src.tools.hashed_func import Hasher
from src.tools.security import USER_ROLE
from src.utils.celery.celery_tasks import sender_email_task
from jose import jwt, JWTError
from decouple import config
from datetime import datetime
from datetime import timezone

router = APIRouter()

@router.get(
    "/confirm_email",
    status_code=status.HTTP_201_CREATED,
    response_model=UserDTOGet,
)
async def sign_up_user(token: str, session: AsyncSession = Depends(get_async_db)):
    try:
        data = jwt.decode(token=token, algorithms=config("ALGORITM_JWT"),
                          key=config("SECRET_KEY_JWT"))
        query = await session.execute(select(User).where(User.id == data.get("id")))
        obj = query.scalar_one_or_none()
        obj.is_active = True
        obj.activated_at = datetime.now(timezone.utc)
        await session.commit()

    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid token")

    except Exception as exp:
        return Response(content=f"{exp}",
                        status_code=422)
    
    return Response(content=f"Email successfully confirmed",
                    status_code=status.HTTP_201_CREATED)