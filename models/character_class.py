from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base

class CharacterClass(Base, table=True):
    __tablename__ = 'character_classes'

    name: str = Field(nullable=True, default="No Name Found")
    hit_die: int = Field(nullable=True, default=6)
    bab_progression: int = Field(nullable=True, default=0)
    fort_progression: int = Field(nullable=True, default=0)
    ref_progression: int = Field(nullable=True, default=0)
    will_progression: int = Field(nullable=True, default=0)
    skill_points: int = Field(nullable=True, default=2)
    class_skills: list = Field(sa_type=JSONB, nullable=True, default=[])
    proficiencies: list = Field(sa_type=JSONB, nullable=True, default=[])
    caster_type_id: Optional[int] = Field(default=None, foreign_key="caster_types.id")