from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
)

from app.core.db import BaseModel


class Donation(BaseModel):
    comment = Column(Text)
    user_id = Column(
        Integer,
        ForeignKey("user.id", name="user_donation"),
    )
