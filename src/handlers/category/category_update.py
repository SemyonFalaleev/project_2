from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from src.dto.category_dto import CategoryDTOUpdate, CategoryDTOGetMin
from src.db.init_db import AsyncSession, get_async_db
from src.db.models import Category
from sqlalchemy.exc import IntegrityError
from fastapi.responses import Response

router = APIRouter()


@router.patch(
    "/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryDTOGetMin
)
async def update_category(
    category_id: int,
    data: CategoryDTOUpdate,
    session: AsyncSession = Depends(get_async_db),
) -> CategoryDTOGetMin:
    try:
        result = await session.execute(
            select(Category).where(Category.id == category_id)
        )
        obj = result.scalar_one_or_none()

        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(obj, field, value)

        session.add(obj)

        await session.commit()
        await session.refresh(obj)

        return CategoryDTOGetMin.model_validate(obj, from_attributes=True)
    except IntegrityError:
        return Response(
            content="A category with such name already exists",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except HTTPException:
        raise
