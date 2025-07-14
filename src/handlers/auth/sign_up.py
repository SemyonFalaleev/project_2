from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from src.dto.user_dto import UserSignUpDTO, UserDTOGet
from src.db.init_db import AsyncSession, get_async_db
from src.db.models import User
from sqlalchemy.exc import IntegrityError
from src.tools.hashed_func import Hasher
from src.tools.security import USER_ROLE
from src.utils.celery.celery_tasks import sender_email_task
from src.tools.security import create_email_token
router = APIRouter()

@router.post(
    "/sign_up",
    status_code=status.HTTP_201_CREATED,
    response_model=UserDTOGet,
)
async def sign_up_user(data: UserSignUpDTO, session: AsyncSession = Depends(get_async_db)):
    try:
        hash_pw = Hasher.get_password_hash(data.password.get_secret_value())

        new_user = User(**data.model_dump(exclude={"password"}),
                        hashed_password=hash_pw,
                        role_id = USER_ROLE) 
        
        
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        data = {
            "id" : str(new_user.id)
        }
        sender_email_task.delay(create_email_token(data), new_user.email,
                                "http://0.0.0.0:8000/auth/confirm_email")
    except IntegrityError:
        return Response(content="A user with such data already exists",
                        status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as exp:
        return Response(content=f"{exp}",
                        status_code=422)
    
    return Response(content=f"A confirmation message has been sent to your email: {new_user.email}.",
                    status_code=status.HTTP_201_CREATED)