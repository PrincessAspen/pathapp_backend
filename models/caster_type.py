from sqlmodel import SQLModel, Field
from typing import Optional
from .base import Base

class CasterType(Base, table=True):
    __tablename__="caster_types"
    type_id: Optional[int] = Field(default=None, index=True, nullable=True)
    character_level: Optional[int] = Field(default=None, index=True, nullable=True)  # Level the progression applies to
    
    casting_method: Optional[str] = Field(default=None, index=True, nullable=True)  # Example values: "Spontaneous" or "Prepared"

    # Spell progression columns for each spell level (all nullable)
    spell_level_0: Optional[int] = Field(default=None, nullable=True)
    spell_level_1: Optional[int] = Field(default=None, nullable=True)
    spell_level_2: Optional[int] = Field(default=None, nullable=True)
    spell_level_3: Optional[int] = Field(default=None, nullable=True)
    spell_level_4: Optional[int] = Field(default=None, nullable=True)
    spell_level_5: Optional[int] = Field(default=None, nullable=True)
    spell_level_6: Optional[int] = Field(default=None, nullable=True)
    spell_level_7: Optional[int] = Field(default=None, nullable=True)
    spell_level_8: Optional[int] = Field(default=None, nullable=True)
    spell_level_9: Optional[int] = Field(default=None, nullable=True)

    # Spells known columns for each spell level (all nullable)
    known_spell_level_0: Optional[int] = Field(default=None, nullable=True)
    known_spell_level_1: Optional[int] = Field(default=None, nullable=True)
    known_spell_level_2: Optional[int] = Field(default=None, nullable=True)
    known_spell_level_3: Optional[int] = Field(default=None, nullable=True)
    known_spell_level_4: Optional[int] = Field(default=None, nullable=True)
    known_spell_level_5: Optional[int] = Field(default=None, nullable=True)
    known_spell_level_6: Optional[int] = Field(default=None, nullable=True)
    known_spell_level_7: Optional[int] = Field(default=None, nullable=True)
    known_spell_level_8: Optional[int] = Field(default=None, nullable=True)
    known_spell_level_9: Optional[int] = Field(default=None, nullable=True)
