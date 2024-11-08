from sqlmodel import SQLModel
from .base import Base

class Alignment(Base, table=True):
    __tablename__ = 'alignments'

    name: str
    abbreviation: str