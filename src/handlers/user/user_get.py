from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from src.dto.user_dto import UserDTOGet
from src.db.init_db import AsyncSession, get_async_db
from src.db.models import User
from sqlalchemy.orm import selectinload

router = APIRouter()


@router.get("/{user_uuid}", status_code=status.HTTP_200_OK, response_model=UserDTOGet)
async def get_user(
    user_uuid: UUID, session: AsyncSession = Depends(get_async_db)
) -> UserDTOGet:
    try:
        result = await session.execute(
            select(User)
            .options(selectinload(User.articles))
            .where(User.id == user_uuid)
        )
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return UserDTOGet.model_validate(user, from_attributes=True)

    except HTTPException:
        raise
