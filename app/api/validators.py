from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models.charity_project import CharityProject
from app.crud.charity_project import charity_project_crud


async def check_charity_project_exist(
    obj_id: int, session: AsyncSession
) -> CharityProject:
    instance = await charity_project_crud.get(obj_id, session)
    if instance is None:
        raise HTTPException(
            status_code=422, detail="Сбор пожертвований не найден"
        )
    return instance


async def check_project_unique_name(name: str, session: AsyncSession) -> None:
    instance = await charity_project_crud.get_by_any_field(name, session)
    if instance:
        raise HTTPException(
            status_code=400, detail="Проект с таким именем уже существует!"
        )


def check_availablesum_size(donation, full_sum, invested_sum):
    pass


async def check_project_on_delete_available(
    obj: CharityProject
) -> None:
    if obj.invested_amount != 0 or obj.close_date is not None:
        raise HTTPException(
            status_code=400, detail="В проект были внесены средства, не подлежит удалению!"
        )


async def check_project_new_sum(instance: CharityProject, new_sum: int):
    if new_sum < instance.invested_amount:
        raise HTTPException(
            status_code=422, detail='Невозможно изменить сумму проекта на значение меньше - уже собранной.'
        )


async def check_project_isnot_closed(instance: CharityProject):
    if instance.close_date is not None:
        raise HTTPException(
            status_code=400, detail='Закрытый проект нельзя редактировать!'
        )
