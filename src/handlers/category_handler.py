from fastapi import APIRouter, Depends, status
from src.dto.category_dto import (
    CategoryDTOCreate,
    CategoryDTOGet,
    CategoryDTOGetAll,
    CategoryDTOGetMin,
    CategoryDTOUpdate,
)
from src.deps.category_dependency import get_category_service
from src.services.category_service import CategoryService

router = APIRouter(prefix="/category", tags=["Category"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryDTOGetMin,
)
async def create_category(
    data: CategoryDTOCreate, service: CategoryService = Depends(get_category_service)
):
    return await service.create(data)


@router.get("/", status_code=status.HTTP_200_OK, response_model=CategoryDTOGetAll)
async def get_all_category(
    service: CategoryService = Depends(get_category_service),
) -> CategoryDTOGetAll:
    return await service.get_all()


@router.get(
    "/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryDTOGet
)
async def get_category(
    category_id: int, service: CategoryService = Depends(get_category_service)
) -> CategoryDTOGet:
    return await service.get_category(category_id)


@router.delete(
    "/{category_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_category(
    category_id: int, service: CategoryService = Depends(get_category_service)
) -> None:
    return await service.delete(category_id)


@router.patch(
    "/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryDTOGetMin
)
async def update_category(
    category_id: int,
    data: CategoryDTOUpdate,
    service: CategoryService = Depends(get_category_service),
) -> CategoryDTOGetMin:
    return await service.update(category_id, data)
