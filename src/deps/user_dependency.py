from fastapi import Depends
from src.db.init_db import get_async_db
from src.repositories.user_repository import UserRepository


async def get_user_repo(session=Depends(get_async_db)):
    return UserRepository(session)
