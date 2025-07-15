from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from src.db.models.category_model import Category
from src.dto.category_dto import CategoryDTOCreate, CategoryDTOGetMin
from src.db.init_db import AsyncSession, get_async_db
from sqlalchemy.exc import IntegrityError

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryDTOGetMin,
)
async def create_category(
    data: CategoryDTOCreate, session: AsyncSession = Depends(get_async_db)
):
    try:
        new_obj = Category(**data.model_dump())
        session.add(new_obj)
        await session.commit()
        await session.refresh(new_obj)
    except IntegrityError:
        return Response(
            content="A category with such name already exists",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as exp:
        return Response(content=f"{exp}", status_code=422)

    return new_obj
