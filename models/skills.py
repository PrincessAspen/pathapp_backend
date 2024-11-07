from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional, Dict
from .base import Base

class Skill(Base, table=True):
    __tablename__ = 'skills'

    name: str = Field(nullable=True)
    modifying_stat: int = Field(nullable=True, default=0)  # 0 could represent "None" or a default stat
    untrained: bool = Field(nullable=True, default=False)