from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from src.dto.user_dto import UserDTOUpdate, UserDTOGet
from src.db.init_db import AsyncSession, get_async_db
from src.db.models import User
from sqlalchemy.exc import IntegrityError
from fastapi.responses import Response

router = APIRouter()


@router.patch("/{user_uuid}", status_code=status.HTTP_200_OK, response_model=UserDTOGet)
async def patch_user(
    user_uuid: UUID, data: UserDTOUpdate, session: AsyncSession = Depends(get_async_db)
) -> UserDTOGet:
    try:
        result = await session.execute(select(User).where(User.id == user_uuid))
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return UserDTOGet.model_validate(user, from_attributes=True)
    except IntegrityError:
        return Response(
            content="A user with such data already exists",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except HTTPException:
        raise
