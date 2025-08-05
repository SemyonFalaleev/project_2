from fastapi import Depends
from src.deps.user_dependency import get_user_repo
from src.services.auth_service import AuthService


async def get_auth_service(repo=Depends(get_user_repo)):
    return AuthService(repo)
