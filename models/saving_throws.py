from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base

class SavingThrowProgression(Base, table=True):
    __tablename__ = 'saving_throw_progressions'

    progression_type: str = Field( default="Poor")
    values: dict = Field(sa_type=JSONB, nullable=True, default={})