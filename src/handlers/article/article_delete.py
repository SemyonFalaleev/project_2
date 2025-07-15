from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from src.db.init_db import AsyncSession, get_async_db
from src.db.models import Article, ArchivedArticle
from fastapi.responses import Response
from src.dto.article_dto import ArchivedArticleDTOCreate

router = APIRouter()


@router.delete(
    "/{article_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_article(
    article_id: int, session: AsyncSession = Depends(get_async_db)
) -> None:
    try:
        result = await session.execute(select(Article).where(Article.id == article_id))
        obj = result.scalar_one_or_none()

        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
            )
        archived_article_dto = ArchivedArticleDTOCreate.model_validate(
            obj, from_attributes=True
        )
        archived_article_obj = ArchivedArticle(**archived_article_dto.model_dump())
        session.add(archived_article_obj)
        await session.delete(obj)
        await session.commit()

    except HTTPException as ex:
        return Response(content=f"{ex}", status_code=status.HTTP_400_BAD_REQUEST)

    return None
