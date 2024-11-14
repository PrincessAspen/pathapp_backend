from sqlmodel import Field, SQLModel
from typing import Optional
from .base import Base

class Feat(Base, table=True):
    __tablename__ = 'feats'

    name: str
    description: str = Field(nullable=True, default="")
    numeric_modifier: Optional[float] = Field(nullable=True)
    level_requirement: int = Field(nullable=True, default=1)
    category: str = Field(nullable=True, default="General")