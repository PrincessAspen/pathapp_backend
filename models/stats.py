from sqlmodel import Field, SQLModel, Relationship
from .base import Base


class Stat(Base, table=True):
    __tablename__ = 'stats'

    name: str = Field(nullable=True)
    abbreviation: str = Field(nullable=True)