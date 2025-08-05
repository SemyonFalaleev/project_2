from fastapi import Depends
from src.db.init_db import get_async_db
from src.repositories.article_repository import ArticleRepository
from src.services.article_service import ArticleService


async def get_article_repo(session=Depends(get_async_db)):
    return ArticleRepository(session)


async def get_article_service(repo=Depends(get_article_repo)):
    return ArticleService(repo)
