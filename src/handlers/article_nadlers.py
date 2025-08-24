from fastapi import APIRouter, Depends, Request, status, File
from fastapi import UploadFile
from src.dto.article_dto import (
    ArticleDTOGet,
    ArticleDTOGetMin,
    ArticleDTOCreate,
    ArticleDTOUpdate,
)
from src.deps.article_dependency import get_article_service
from src.dto.filters.article_filters import ArticleFilters
from src.dto.pagination_dto import PaginatedResponse
from src.services.article_service import ArticleService
from src.tools.pagination import PaginatorParams

router = APIRouter(prefix="/article", tags=["Article"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ArticleDTOGetMin,
)
async def create_article(
    cover_image: UploadFile,
    request: Request,
    data: ArticleDTOCreate = Depends(ArticleDTOCreate.as_form),
    service: ArticleService = Depends(get_article_service),
):
    return await service.create_article(
        data, cover_image, request.state.user.get("user_id")
    )


@router.delete(
    "/{article_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_article(
    article_id: int, service: ArticleService = Depends(get_article_service)
) -> None:
    return await service.delete_article_by_id(article_id)


@router.get("/", status_code=status.HTTP_200_OK, response_model=PaginatedResponse)
async def get_all_articles(
    filters: ArticleFilters = Depends(),
    paginator: PaginatorParams = Depends(),
    service: ArticleService = Depends(get_article_service),
) -> PaginatedResponse:
    return await service.article_get_all(filters, paginator)


@router.get(
    "/{article_id}", status_code=status.HTTP_200_OK, response_model=ArticleDTOGet
)
async def get_articles(
    article_id: int, service: ArticleService = Depends(get_article_service)
) -> ArticleDTOGet:
    return await service.get_article(article_id)


@router.patch(
    "/{article_id}", status_code=status.HTTP_200_OK, response_model=ArticleDTOGetMin
)
async def update_article(
    article_id: int,
    article_data: ArticleDTOUpdate = Depends(ArticleDTOUpdate.as_form),
    cover_image: UploadFile | None = File(default=None),
    service: ArticleService = Depends(get_article_service),
):
    return await service.update_article(article_id, cover_image, article_data)
