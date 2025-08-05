from fastapi import Depends
from src.db.init_db import get_async_db
from src.repositories.category_repository import CategoryRepository
from src.services.category_service import CategoryService


async def get_category_repo(session=Depends(get_async_db)):
    return CategoryRepository(session)


async def get_category_service(repo=Depends(get_category_repo)):
    return CategoryService(repo)
