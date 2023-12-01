from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, Extra


class CharityProjectBase(BaseModel):
    name: str = Field(None, max_length=100, min_length=1)
    description: str = Field(None, min_length=1)
    full_amount: int = Field(None, gt=0)


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)


class CharityProjectList(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):

    class Config:
        extra = Extra.forbid
