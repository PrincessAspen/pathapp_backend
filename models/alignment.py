from sqlmodel import Field, SQLModel, Relationship
from .base import Base

class Alignment(Base, table=True):
    __tablename__ = 'alignments'

    name: str
    abbreviation: str