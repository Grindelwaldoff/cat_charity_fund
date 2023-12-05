from datetime import datetime

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Boolean

from app.core.db import Base


class Donation(Base):
    comment = Column(Text)
    full_amount = Column(Integer, nullable=False,)
    create_date = Column(DateTime, default=datetime.now,)
    close_date = Column(DateTime,)
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='user_donation'),
    )
    invested_amount = Column(Integer, default=0,)
    fully_invested = Column(Boolean, default=False,)

    def invested(self):
        self.fully_invested = True
        self.close_date = datetime.now()
        self.invested_amount = self.full_amount
