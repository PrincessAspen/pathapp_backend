from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from .base import Base

class RacialTrait(Base, table=True):
    __tablename__ = 'racial_traits'

    category: str = Field(nullable=True, default="General")
    description: str = Field(nullable=True, default="")
    numeric_modifier: Optional[float] = Field(nullable=True)