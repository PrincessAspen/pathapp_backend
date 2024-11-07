from sqlmodel import Field, SQLModel, Relationship
from .base import Base

class MoneyValue(Base, table=True):
    __tablename__ = 'money_values'

    platinum: float = Field(nullable=True, default=10)
    gold: float = Field(nullable=True, default=1)
    electrum: float = Field(nullable=True, default=0.5)
    silver: float = Field(nullable=True, default=0.1)
    copper: float = Field(nullable=True, default=0.01)