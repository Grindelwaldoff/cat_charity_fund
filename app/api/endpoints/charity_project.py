from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.charity_project import (
    CharityProjectList,
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.crud.charity_project import charity_project_crud
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.api.validators import (
    check_charity_project_exist,
    check_project_unique_name,
    check_project_on_delete_available,
    check_project_new_sum,
    check_project_isnot_closed,
)
from app.models.donation import Donation


router = APIRouter()


@router.get(
    "/",
    response_model=list[CharityProjectList],
    response_model_exclude_none=True,
)
async def list_projects(session: AsyncSession = Depends(get_async_session)):
    return await charity_project_crud.get_multi(session)


@router.delete(
    "/{project_id}",
    response_model=CharityProjectList,
    dependencies=[Depends(current_superuser)],
)
async def delete_projects(
    project_id: int, session: AsyncSession = Depends(get_async_session)
):
    instance = await check_charity_project_exist(project_id, session)
    await check_project_on_delete_available(instance)
    return await charity_project_crud.remove(instance, session)


@router.post(
    "/",
    response_model=CharityProjectList,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_project_unique_name(charity_project.name, session)
    return await charity_project_crud.create(
        charity_project, session, Donation
    )


@router.patch(
    "/{project_id}",
    response_model=CharityProjectList,
    dependencies=[Depends(current_superuser)],
)
async def update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    instance = await check_charity_project_exist(project_id, session)
    await check_project_isnot_closed(instance)
    if obj_in.name is not None:
        await check_project_unique_name(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_project_new_sum(instance, obj_in.full_amount)
    return await charity_project_crud.update(instance, obj_in, session)
