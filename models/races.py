from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base

class Race(Base, table=True):
    __tablename__ = 'races'

    name: str = Field(nullable=True)
    stat_modifiers: dict = Field(sa_type=JSONB, nullable=True, default={})
    size_category: str = Field(nullable=True, default="Medium")
    starting_languages: list = Field(sa_type=JSONB, nullable=True, default=[])