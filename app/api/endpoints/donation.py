from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.donation import (
    DonationList,
    DonationCreate,
    UsersDonationList,
)
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.models import User
from app.services.investment import donation_investment_calculation
from app.crud.donation import donation_crud


router = APIRouter()


@router.post(
    "/", response_model=UsersDonationList, response_model_exclude_none=True
)
async def donate(
    obj_in: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    instance = await donation_crud.create(obj_in, session, user)
    await donation_investment_calculation(instance, session)
    return instance


@router.get("/my", response_model=list[UsersDonationList])
async def list_users_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_users_donation(user, session)


@router.get(
    "/",
    response_model=list[DonationList],
    dependencies=[Depends(current_superuser)],
)
async def list_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi(session)
