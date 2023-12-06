from typing import TypeVar, Generic, Type, Optional, List

from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, false
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User
from app.services.investment import investment


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
        self, obj_id: int, session: AsyncSession
    ) -> Optional[ModelType]:
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession, **kwargs) -> List[ModelType]:
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def remove(
        self, db_obj: ModelType, session: AsyncSession
    ) -> ModelType:
        session.delete(db_obj)
        session.commit()
        return db_obj

    async def create(
        self,
        obj_in: CreateSchemaType,
        session: AsyncSession,
        cls_in,
        user: Optional[User] = None,
    ) -> ModelType:
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        instance = self.model(**obj_in_data)
        instance.invested_amount = 0
        non_unfilled = await session.execute(
            select(cls_in).where(cls_in.fully_invested == false())
        )
        objects = investment(
            instance,
            non_unfilled.scalars().all()
        )
        session.add_all(objects)
        await session.commit()
        await session.refresh(instance)
        return instance

    async def get_by_name(self, name: str, session: AsyncSession):
        obj = await session.execute(
            select(self.model).where(self.model.name == name)
        )
        return obj.scalars().first()

    async def get_users_donation(self, user: User, session: AsyncSession):
        objs = await session.execute(
            select(self.model).where(self.model.user_id == user.id)
        )
        return objs.scalars().all()

    async def update(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        session: AsyncSession,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
