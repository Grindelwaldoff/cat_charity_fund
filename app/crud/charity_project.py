from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.models.charity_project import CharityProject


class CRUDCharity(CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]):
    async def get_by_name(self, name: str, session: AsyncSession):
        obj = await session.execute(
            select(CharityProject).where(CharityProject.name == name)
        )
        return obj.scalars().first()


charity_project_crud = CRUDCharity(CharityProject)
