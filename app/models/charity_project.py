from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime

from app.core.db import Base


class CharityProject(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0,)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(
        DateTime, default=datetime.now
    )
    close_date = Column(DateTime)

    def invested(self):
        self.fully_invested = True
        self.close_date = datetime.now()
        self.invested_amount = self.full_amount
