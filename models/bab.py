from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base

class BABProgression(Base, table=True):
    __tablename__ = 'bab_progressions'

    progression_type: str = Field(nullable=True, default="Poor")
    values: dict = Field(sa_type=JSONB, nullable=True, default={})