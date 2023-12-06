from sqlalchemy import Column, String, Text

from app.core.db import BaseModel
from app.core.config import settings


class CharityProject(BaseModel):
    name = Column(String(settings.STRING_LENGTH), unique=True, nullable=False)
    description = Column(Text)
