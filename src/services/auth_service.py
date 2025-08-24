from fastapi import HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from src.db.models.user_model import User
from src.dto.user_dto import UserSignUpDTO
from src.dto.validation_func import validate_email, validate_phone
from src.repositories.user_repository import UserRepository
from src.tools.hashed_func import Hasher
from src.tools.security import USER_ROLE, create_access_token, create_email_token
from src.utils.celery.celery_tasks import sender_email_task
from sqlalchemy.exc import IntegrityError
from jose import jwt
from decouple import config
from datetime import datetime, timezone


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def sign_up(self, data: UserSignUpDTO) -> Response:
        hash_pw = Hasher.get_password_hash(data.password.get_secret_value())

        new_user_data = User(
            **data.model_dump(exclude={"password"}),
            hashed_password=hash_pw,
            role_id=USER_ROLE,
        )

        try:
            user_obj = await self.repo.create(new_user_data)

        except IntegrityError:
            raise HTTPException(
                detail="A user with such data already exists",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        payload = {"id": str(user_obj.id)}

        sender_email_task.delay(
            create_email_token(payload),
            user_obj.email,
            "http://0.0.0.0:8000/auth/confirm_email",
        )
        return Response(
            content=f"A confirmation message has been sent to your email: {user_obj.email}.",
            status_code=status.HTTP_201_CREATED,
        )

    async def sign_in(self, data: OAuth2PasswordRequestForm) -> Response:
        if email := validate_email(data.username):
            obj = await self.repo.get_by_email(email)
        elif phone_number := validate_phone(data.username):
            obj = await self.repo.get_by_phone(phone_number)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please enter a valid email or phone number",
            )
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with such data not found",
            )
        if Hasher.verify_password(data.password, obj.hashed_password):
            access_token = create_access_token(
                data={"id": str(obj.id), "role_id": obj.role_id}
            )
            response = Response(
                content=("Login successful"), status_code=status.HTTP_200_OK
            )
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,
                samesite="lax",
                max_age=60 * 10,
            )
            return response
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="WRONG PASSWORD"
            )

    async def confirm_email(self, token: str) -> Response:
        try:
            data = jwt.decode(
                token=token,
                algorithms=config("ALGORITM_JWT"),
                key=config("SECRET_KEY_JWT"),
            )
            obj = await self.repo.get_by_id(data.get("id"))
            await self.repo.change_user_activity(obj, datetime.now(timezone.utc))

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
            )

        return Response(
            content="Email successfully confirmed", status_code=status.HTTP_201_CREATED
        )
