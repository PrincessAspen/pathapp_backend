from sqlmodel import Field, SQLModel
from typing import Optional
from .base import Base

class Skill(Base, table=True):
    __tablename__ = 'skills'

    name: str = Field(nullable=True)
    modifying_stat_id: Optional[int] = Field(default=None, foreign_key="stats.id")
    untrained: bool = Field(nullable=True, default=False)