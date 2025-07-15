from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from src.dto.article_dto import ArticleDTOGetMin
from src.db.init_db import AsyncSession, get_async_db
from src.db.models import Article
from src.dto.pagination_dto import PaginatedResponse
from src.dto.filters.article_filters import ArticleFilters
from src.tools.pagination import PaginatorParams

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=PaginatedResponse)
async def get_all_articles(
    filters: ArticleFilters = Depends(),
    paginator: PaginatorParams = Depends(),
    session: AsyncSession = Depends(get_async_db),
) -> PaginatedResponse:
    try:
        query = select(Article)

        if filters.search:
            query = query.where(Article.name.ilike(f"%{filters.search}%"))
        if filters.category_id:
            query = query.where(Article.category_id == filters.category_id)

        total_result = await session.execute(query)
        total = len(total_result.scalars().all())

        query = query.offset(paginator.offset).limit(paginator.limit)
        result = await session.execute(query)
        articles = result.scalars().all()

        if articles is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
            )

        return PaginatedResponse[ArticleDTOGetMin](
            count=total,
            page=paginator.page,
            limit=paginator.limit,
            results=[
                ArticleDTOGetMin.model_validate(obj, from_attributes=True)
                for obj in articles
            ],
        )

    except HTTPException:
        raise
