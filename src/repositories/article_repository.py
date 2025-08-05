from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.db.models import Article
from src.db.models.article_model import ArchivedArticle
from src.dto.filters.article_filters import ArticleFilters
from typing import List


class ArticleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _build_query_filter(self, filters: ArticleFilters = None) -> select:
        query = select(Article)

        if filters is None:
            return query

        if filters.search:
            query = query.where(Article.name.ilike(f"%{filters.search}%"))

        if filters.category_id:
            query = query.where(Article.category_id == filters.category_id)

        return query

    async def create(self, article: Article) -> Article:
        self.session.add(article)
        await self.session.commit()
        await self.session.refresh(article)
        return article

    async def create_archived(
        self, archived_article: ArchivedArticle
    ) -> ArchivedArticle:
        self.session.add(archived_article)
        await self.session.commit()
        await self.session.refresh(archived_article)
        return archived_article

    async def get_by_id_with_related(self, id: int) -> Article | None:
        stmt = (
            select(Article)
            .options(selectinload(Article.category), selectinload(Article.user))
            .where(Article.id == id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, obj: Article) -> None:
        await self.session.delete(obj)
        await self.session.commit()

    async def get_by_id(self, id: int) -> Article | None:
        query = await self.session.execute(select(Article).where(Article.id == id))
        return query.scalar_one_or_none()

    async def get_all_filtered_paginate(
        self, filters: ArticleFilters, offset: int, limit: int
    ) -> List[Article]:
        query = self._build_query_filter(filters).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def count_filtered(self, filters: ArticleFilters) -> int:
        query = self._build_query_filter(filters)
        result = await self.session.execute(query)
        return len(result.scalars().all())

    async def update(self, article: Article) -> Article:
        self.session.add(article)
        await self.session.commit()
        await self.session.refresh(article)
        return article
