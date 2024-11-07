from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from .base import Base

class Armor(Base, table=True):
    __tablename__ = 'armor'

    name: str = Field(nullable=True)  # Added missing name field
    category: str = Field(nullable=True, default="Light")
    material: Optional[str] = Field(nullable=True)
    cost: float = Field(nullable=True, default=0.0)
    armor_bonus: float = Field(nullable=True, default=0.0)
    max_dex_bonus: float = Field(nullable=True, default=999.0)  # Using 999 to represent "unlimited"
    armor_check_penalty: float = Field(nullable=True, default=0.0)
    arcane_spell_failure: float = Field(nullable=True, default=0.0)
    max_speed: float = Field(nullable=True, default=30.0)
    weight: float = Field(nullable=True, default=0.0)