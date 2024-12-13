from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base

class CharacterClass(Base, table=True):
    __tablename__ = 'character_classes'

    name: str = Field(nullable=True, default="No Name Found")
    hit_die: int = Field(nullable=True, default=6)
    bab_progression: str = Field(nullable=True, default="low")
    fort_progression: str = Field(nullable=True, default="poor_save")
    ref_progression: str = Field(nullable=True, default="poor_save")
    will_progression: str = Field(nullable=True, default="poor_save")
    skill_points: int = Field(nullable=True, default=2)
    class_skills: list = Field(sa_type=JSONB, nullable=True, default=[])
    proficiencies: list = Field(sa_type=JSONB, nullable=True, default=[])
    caster_type_id: Optional[int] = Field(default=None, foreign_key="caster_types.id")
    starting_spells: list = Field(sa_type=JSONB, nullable=True)
    starting_weapons: list = Field(sa_type=JSONB, nullable=True)
    starting_armor: list = Field(sa_type=JSONB, nullable=True)
    starting_inventory: list = Field(sa_type=JSONB, nullable=True)
    casting_stat: Optional[int] = Field(default=None, nullable=True, foreign_key="stats.id")