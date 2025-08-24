from fastapi import HTTPException, UploadFile
from fastapi import status
from src.db.models.article_model import ArchivedArticle, Article
from src.dto.article_dto import (
    ArchivedArticleDTOCreate,
    ArticleDTOCreate,
    ArticleDTOGet,
    ArticleDTOGetMin,
    ArticleDTOUpdate,
)
from src.dto.filters.article_filters import ArticleFilters
from src.dto.pagination_dto import PaginatedResponse
from src.repositories.article_repository import ArticleRepository
from src.tools.pagination import PaginatorParams
from src.utils.aws_interface import client_s3
from sqlalchemy.exc import IntegrityError


class ArticleService:
    def __init__(self, repo: ArticleRepository):
        self.repo = repo

    async def create_article(
        self, data: ArticleDTOCreate, cover_image: UploadFile, user_id: int
    ) -> ArticleDTOGetMin:
        cover_image_url = client_s3.upload_file_from_stream(cover_image)

        data_dict = data.model_dump(exclude={"cover_image_url", "user_id"})

        article_obj = Article(
            **data_dict,
            cover_image_url=cover_image_url,
            user_id=user_id,
        )

        try:
            new_obj = await self.repo.create(article_obj)
        except IntegrityError:
            client_s3.delete_file_from_bucket(article_obj.cover_image_url)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect category id specified",
            )

        return ArticleDTOGetMin.model_validate(new_obj, from_attributes=True)

    async def delete_article_by_id(self, id: int):
        obj = await self.repo.get_by_id(id)
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
            )
        archived_article_dto = ArchivedArticleDTOCreate.model_validate(
            obj, from_attributes=True
        )
        archived_article_obj = ArchivedArticle(**archived_article_dto.model_dump())
        await self.repo.delete(obj)
        await self.repo.create_archived(archived_article_obj)
        return None

    async def article_get_all(
        self, filters: ArticleFilters, paginator: PaginatorParams
    ) -> PaginatedResponse:
        total = await self.repo.count_filtered(filters)
        total_result = await self.repo.get_all_filtered_paginate(
            filters, paginator.offset, paginator.limit
        )
        return PaginatedResponse(
            count=total,
            page=paginator.page,
            limit=paginator.limit,
            results=[
                ArticleDTOGetMin.model_validate(obj, from_attributes=True)
                for obj in total_result
            ],
        )

    async def get_article(self, id: int):
        article_obj = await self.repo.get_by_id_with_related(id)
        if article_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
            )
        article_dto = ArticleDTOGet.model_validate(article_obj, from_attributes=True)
        return article_dto

    async def update_article(
        self, id: int, cover_image: UploadFile, article_dto: ArticleDTOUpdate
    ) -> ArticleDTOGetMin:
        article_obj = await self.repo.get_by_id(id)
        if article_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Article with {id} not found",
            )
        if cover_image:
            old_cover_image_url = article_obj.cover_image_url
            new_cover_image_url = client_s3.upload_file_from_stream(cover_image)
            article_dto.cover_image_url = new_cover_image_url

        update_data = article_dto.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is None:
                continue
            setattr(article_obj, field, value)
        try:
            new_obj = await self.repo.update(article_obj)
        except IntegrityError:
            client_s3.delete_file_from_bucket(new_cover_image_url)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect category id specified",
            )
        else:
            client_s3.delete_file_from_bucket(old_cover_image_url)
        return ArticleDTOGetMin.model_validate(new_obj, from_attributes=True)
