from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from .base import Base

class Weapon(Base, table=True):
    __tablename__ = 'weapons'

    name: str = Field(nullable=True)  # Added missing name field
    category: str = Field(nullable=True, default="Simple")
    type: str = Field(nullable=True, default="Melee")
    damage_dice: str = Field(nullable=True, default="1d4")
    damage_type: str = Field(nullable=True, default="Bludgeoning")
    material: Optional[str] = Field(nullable=True)
    range: Optional[float] = Field(nullable=True)
    reach: Optional[float] = Field(nullable=True)
    special_properties: Optional[str] = Field(nullable=True)
    weight: float = Field(nullable=True, default=1.0)
    numeric_modifier: Optional[float] = Field(nullable=True)
    gold_value: Optional[float] = Field(nullable=True)