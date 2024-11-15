from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base

class Spell(Base, table=True):
    __tablename__ = 'spells'

    name: str = Field(nullable=True)  # Added missing name field
    spell_level: int = Field(nullable=True, default=0)
    class_lists: list = Field(sa_type=JSONB, nullable=True, default=[])
    material_component: Optional[str] = Field(nullable=True)
    somatic_component: Optional[str] = Field(nullable=True)
    verbal_component: Optional[str] = Field(nullable=True)
    school: str = Field(nullable=True, default="Universal")
    description: str = Field(nullable=True, default="")
    allows_save: bool = Field(nullable=True, default=False)