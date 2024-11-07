from sqlmodel import Relationship, Column
from sqlalchemy import Column, Integer, String, Float
from .base import Base

class ClassAbility(Base, table=True):
    __tablename__ = "class_abilities"
    
    name: str = Column(String, nullable=True)
    description: str = Column(String, nullable=True)
    level_requirement: int = Column(Integer, nullable=True)
    numeric_modifier: float = Column(Float, nullable=True)
    category: str = Column(String, nullable=True)