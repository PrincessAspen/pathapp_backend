from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from .base import Base

class Equipment(Base, table=True):
    __tablename__ = 'equipment'

    name: str
    gold_value: Optional[float] = Field(nullable=True)
    container: bool = Field(nullable=True, default=False)
    category: str = Field(nullable=True, default="Miscellaneous")
    rarity: str = Field(nullable=True, default="Common")
    numeric_modifier: Optional[float] = Field(nullable=True)
    weight: float = Field( default=0.0)