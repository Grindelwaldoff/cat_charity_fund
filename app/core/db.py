from datetime import datetime

from sqlalchemy.orm import declarative_base, sessionmaker, declared_attr
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Boolean,
    CheckConstraint,
)

from app.core.config import settings


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)


class BaseModel(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint("full_amount >= invested_amount"),
        CheckConstraint("0 < full_amount"),
    )
    full_amount = Column(
        Integer,
        nullable=False,
    )
    create_date = Column(
        DateTime,
        default=datetime.now,
    )
    close_date = Column(
        DateTime,
    )
    invested_amount = Column(
        Integer,
        default=settings.INT_DEFAULT_VALUE,
    )
    fully_invested = Column(
        Boolean,
        default=False,
    )

    def invested(self):
        self.fully_invested = True
        self.close_date = datetime.now()
        self.invested_amount = self.full_amount


engine = create_async_engine(settings.database_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
