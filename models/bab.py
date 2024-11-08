from sqlmodel import Field, SQLModel
from .base import Base

class BABProgression(Base, table=True):
    __tablename__ = 'bab_progressions'

    level: int = Field(nullable=True, default=1)
    high: int = Field(nullable=True, default=1)
    medium: int = Field(nullable=True, default=0)
    low: int = Field(nullable=True, default=0)