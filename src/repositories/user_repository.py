from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.db.models import User
from typing import List
from datetime import datetime


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: User) -> User:
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def update(self, data: User) -> User:
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def get_by_id(self, id: int) -> User | None:
        query = await self.session.execute(select(User).where(User.id == id))
        return query.scalar_one_or_none()

    async def get_by_id_with_realted(self, id: int) -> User | None:
        query = await self.session.execute(
            select(User).options(selectinload(User.articles)).where(User.id == id)
        )
        return query.scalar_one_or_none()

    async def get_all(self) -> List[User]:
        query = await self.session.execute(select(User))
        return query.scalars().all()

    async def get_by_email(self, email: EmailStr, is_active: bool = True) -> User:
        query = select(User).where(User.email == email, User.is_active == is_active)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_phone(
        self, phone_number: PhoneNumber, is_active: bool = True
    ) -> User:
        query = select(User).where(
            User.phone_number == phone_number, User.is_active == is_active
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def change_user_activity(
        self, user: User, activated_at: datetime, is_active: bool = True
    ) -> User:
        user.is_active = is_active
        user.activated_at = activated_at
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
