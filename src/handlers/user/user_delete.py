from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from src.db.init_db import AsyncSession, get_async_db
from src.db.models import User

router = APIRouter()


@router.delete(
    "/{user_uuid}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_user(
    user_uuid: UUID, session: AsyncSession = Depends(get_async_db)
) -> None:
    try:
        result = await session.execute(select(User).where(User.id == user_uuid))
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        await session.delete(user)
        await session.commit()

    except HTTPException:
        raise

    return None
