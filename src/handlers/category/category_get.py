from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.dto.category_dto import CategoryDTOGet
from src.db.init_db import AsyncSession, get_async_db
from src.db.models import Category

router = APIRouter()


@router.get(
    "/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryDTOGet
)
async def get_category(
    category_id: int, session: AsyncSession = Depends(get_async_db)
) -> CategoryDTOGet:
    try:
        result = await session.execute(
            select(Category)
            .options(selectinload(Category.articles))
            .where(Category.id == category_id)
        )
        obj = result.scalar_one_or_none()

        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return CategoryDTOGet.model_validate(obj, from_attributes=True)

    except HTTPException:
        raise
