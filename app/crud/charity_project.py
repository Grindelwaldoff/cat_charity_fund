from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.models.charity_project import CharityProject


class CRUDCharity(
    CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]
):
    async def get_by_any_field(
        self, value: str, session: AsyncSession
    ) -> Optional[int]:
        instance = await session.execute(
            select(CharityProject).where(self.model.name == value)
        )
        return instance.scalars().first()


charity_project_crud = CRUDCharity(CharityProject)
