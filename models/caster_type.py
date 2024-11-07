from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base

class CasterType(Base, table=True):
    __tablename__ = 'caster_types'

    name: str
    focus_type: str = Field(nullable=True, default="None")  # Divine, Arcane, etc.
    caster_type: str = Field(nullable=True, default="None")  # Spontaneous, Prepared
    preparation_type: str = Field(nullable=True, default="None")  # Daily, At-will, etc.
    spells_per_day: dict = Field(sa_type=JSONB, nullable=True, default={})
    spells_known: dict = Field(sa_type=JSONB, nullable=True, default={})