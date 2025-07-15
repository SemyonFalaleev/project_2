from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from src.dto.category_dto import CategoryDTOGetAll, CategoryDTOGetMin
from src.db.init_db import AsyncSession, get_async_db
from src.db.models import Category

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=CategoryDTOGetAll)
async def get_all_category(
    session: AsyncSession = Depends(get_async_db),
) -> CategoryDTOGetAll:
    try:
        result = await session.execute(select(Category))
        objs = result.scalars().all()

        if objs is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return CategoryDTOGetAll(
            count=len(objs),
            categories=[
                CategoryDTOGetMin.model_validate(obj, from_attributes=True)
                for obj in objs
            ],
        )

    except HTTPException:
        raise
