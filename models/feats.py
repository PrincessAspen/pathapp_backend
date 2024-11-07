from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional, Dict
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base

class Feat(Base, table=True):
    __tablename__ = 'feats'

    name: str
    description: str = Field(nullable=True, default="")
    numeric_modifier: Optional[float] = Field(nullable=True)
    level_requirement: int = Field(nullable=True, default=1)
    prerequisites: list = Field(sa_type=JSONB, nullable=True, default=[])