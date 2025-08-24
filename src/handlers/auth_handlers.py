from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from src.deps.auth_dependency import get_auth_service
from src.dto.user_dto import UserSignUpDTO
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get(
    "/confirm_email",
    status_code=status.HTTP_201_CREATED,
)
async def confirm_email(token: str, service: AuthService = Depends(get_auth_service)):
    return await service.confirm_email(token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user():
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie(key="access_token", path="/")
    return response


@router.post(
    "/sign_in",
    status_code=status.HTTP_202_ACCEPTED,
)
async def sign_in_user(
    data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    return await service.sign_in(data)


@router.post(
    "/sign_up",
    status_code=status.HTTP_201_CREATED,
)
async def sign_up_user(
    data: UserSignUpDTO, service: AuthService = Depends(get_auth_service)
):
    return await service.sign_up(data)
