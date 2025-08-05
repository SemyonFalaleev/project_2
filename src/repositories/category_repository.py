from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.db.models import Category
from typing import List


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, category: Category) -> Category:
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def delete(self, obj: Category) -> None:
        await self.session.delete(obj)
        await self.session.commit()

    async def get_by_id_with_related(self, id: int) -> Category:
        stmt = (
            select(Category)
            .options(selectinload(Category.articles))
            .where(Category.id == id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, id: int) -> Category | None:
        query = await self.session.execute(select(Category).where(Category.id == id))
        return query.scalar_one_or_none()

    async def update(self, category: Category) -> Category:
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def get_all(self) -> List[Category]:
        query = await self.session.execute(select(Category))
        return query.scalars().all()
