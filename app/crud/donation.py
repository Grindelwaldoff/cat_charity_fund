from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.schemas.donation import DonationCreate


class CRUDDonation(CRUDBase[Donation, DonationCreate, None]):
    async def get_users_donation(self, user: User, session: AsyncSession):
        objs = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return objs.scalars().all()


donation_crud = CRUDDonation(Donation)
