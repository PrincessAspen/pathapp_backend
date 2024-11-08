from sqlmodel import Field, SQLModel
from typing import Optional
from .base import Base

class SavingThrowProgression(Base, table=True):
    __tablename__ = 'saving_throw_progressions'

    level: Optional[int] = Field(default=None, index=True, nullable=True)  # Character level for the progression

    # Columns for save progression
    good_save: Optional[int] = Field(default=None, nullable=True)  # Value for "Good" save progression
    poor_save: Optional[int] = Field(default=None, nullable=True)  # Value for "Poor" save progression