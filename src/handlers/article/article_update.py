from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from src.dto.article_dto import ArticleDTOUpdate, ArticleDTOGetMin
from src.db.init_db import AsyncSession, get_async_db
from src.db.models import Article
from src.utils.aws_interface import client_s3

router = APIRouter()


@router.patch(
    "/{article_id}", status_code=status.HTTP_200_OK, response_model=ArticleDTOGetMin
)
async def update_article(
    article_id: int,
    article_data: ArticleDTOUpdate = Depends(ArticleDTOUpdate.as_form),
    cover_image: UploadFile | None = File(default=None),
    session: AsyncSession = Depends(get_async_db),
):
    query = await session.execute(select(Article).where(Article.id == article_id))
    result = query.scalar_one_or_none()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Article with id: {article_id} not found",
        )
    if cover_image:
        client_s3.delete_file_from_bucket(result.cover_image_url)
        cover_image_url = client_s3.upload_file_from_stream(cover_image)
        article_data.cover_image_url = cover_image_url

    update_data = article_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is None:
            continue
        setattr(result, field, value)
    session.add(result)
    await session.commit()
    await session.refresh(result)
    return ArticleDTOGetMin.model_validate(result, from_attributes=True)
