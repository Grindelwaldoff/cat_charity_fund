from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationBase(BaseModel):
    full_amount: int = Field(gt=0,)
    comment: Optional[str] = None


class DonationCreate(DonationBase):
    pass


class UsersDonationList(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationList(UsersDonationList):
    fully_invested: bool
    invested_amount: int
    user_id: int
