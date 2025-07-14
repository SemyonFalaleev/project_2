from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.dto.article_dto import ArticleDTOGet
from src.db.init_db import AsyncSession, get_async_db
from src.db.models import Article
from decouple import config

router = APIRouter()


@router.get("/{article_id}", status_code=status.HTTP_200_OK, response_model=ArticleDTOGet)
async def get_articlet(
    article_id: int,
    session: AsyncSession = Depends(get_async_db)
) -> ArticleDTOGet:

    try:
        result = await session.execute(select(Article).options(selectinload(Article.category), 
                                                               selectinload(Article.user)).\
                                       where(Article.id == article_id))
        obj = result.scalar_one_or_none()

        if obj == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )
        article_dto = ArticleDTOGet.model_validate(obj, from_attributes=True)
        article_dto.cover_image_url = config("AWS_URL")+"/"+article_dto.cover_image_url
        
        return article_dto
    
    except HTTPException:
        raise