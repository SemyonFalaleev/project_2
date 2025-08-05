from fastapi import HTTPException
from src.db.models.category_model import Category
from src.dto.category_dto import (
    CategoryDTOCreate,
    CategoryDTOGet,
    CategoryDTOGetAll,
    CategoryDTOGetMin,
    CategoryDTOUpdate,
)
from src.repositories.category_repository import CategoryRepository
from fastapi import status
from sqlalchemy.exc import IntegrityError


class CategoryService:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def get_category(self, id: int) -> CategoryDTOGet:
        category_obj = await self.repo.get_by_id_with_related(id)
        if category_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id:{id} not found",
            )
        return CategoryDTOGet.model_validate(category_obj, from_attributes=True)

    async def create(self, category_dto: CategoryDTOCreate) -> CategoryDTOGetMin:
        try:
            obj = Category(**category_dto.model_dump())
            new_obj = await self.repo.create(obj)
            return CategoryDTOGetMin.model_validate(new_obj, from_attributes=True)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A category with such name already exists",
            )

    async def get_all(self) -> CategoryDTOGetAll:
        categories_obj = await self.repo.get_all()
        if categories_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )
        return CategoryDTOGetAll(
            count=len(categories_obj),
            categories=[
                CategoryDTOGetMin.model_validate(category, from_attributes=True)
                for category in categories_obj
            ],
        )

    async def delete(self, id: int) -> None:
        obj = await self.repo.get_by_id(id)
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )
        await self.repo.delete(obj)
        return None

    async def update(
        self, id: int, category_dto: CategoryDTOUpdate
    ) -> CategoryDTOGetMin:
        category_obj = await self.repo.get_by_id(id)
        if category_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )
        update_data = category_dto.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category_obj, field, value)
        try:
            update_obj = await self.repo.update(category_obj)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with such name: {category_dto.name}, alredy exist",
            )

        return CategoryDTOGetMin.model_validate(update_obj, from_attributes=True)
