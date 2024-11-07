from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base

class Language(Base, table=True):
    __tablename__ = 'languages'

    name: str = Field(nullable=True)
    learned_by_races: list = Field(sa_type=JSONB, default=[])