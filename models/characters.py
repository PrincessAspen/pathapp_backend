from sqlmodel import SQLModel, Field, Relationship
from .base import Base
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional

class Character(Base, table=True):
    __tablename__ = "characters"
    name: str = Field(nullable=False)
    level: Optional[int] = Field(default=1)  # Track the character's current level

    user_id: str = Field(nullable=False)

    # Foreign keys for single reference columns
    character_class_id: Optional[int] = Field(default=None, foreign_key="character_classes.id")
    alignment_id: Optional[int] = Field(default=None, foreign_key="alignments.id")
    save_progression_type: Optional[str] = Field(default=None, nullable=True)  # e.g., "Good", "Poor", or a custom string
    feats: Optional[list] = Field(sa_type=JSONB, default=None, nullable=True)
    spells: Optional[list] = Field(sa_type=JSONB, default=None, nullable=True)
    stats: Optional[list] = Field(sa_type=JSONB, default=None, nullable=True)
    skills: Optional[list] = Field(sa_type=JSONB, default=None, nullable=True)
    weapons: Optional[list] = Field(sa_type=JSONB, default=None, nullable=True)
    armor: Optional[list] = Field(sa_type=JSONB, default=None, nullable=True)
    inventory_items: Optional[list] = Field(sa_type=JSONB, default=None, nullable=True)
    money: Optional[list] = Field(sa_type=JSONB, default=None, nullable=True)
    race_id: Optional[int] = Field(default=None, foreign_key="races.id")

    # Relationships without List or cascade delete
    # feats: Optional["CharacterFeatLink"] = Relationship()
    # spells: Optional["CharacterSpellLink"] = Relationship()
    # stats: Optional["CharacterStatLink"] = Relationship()
    # skills: Optional["CharacterSkillLink"] = Relationship()
    # weapons: Optional["CharacterWeaponLink"] = Relationship()
    # armor: Optional["CharacterArmorLink"] = Relationship()
    # inventory_items: Optional["CharacterInventoryLink"] = Relationship()
    # money: Optional["CharacterMoneyLink"] = Relationship()

# Join tables for many-to-many relationships
class CharacterFeatLink(Base, table=True):
    
    character_id: Optional[int] = Field(default=None, foreign_key="characters.id", primary_key=True)
    feat_id: Optional[int] = Field(default=None, foreign_key="feats.id", primary_key=True)

class CharacterSpellLink(Base, table=True):
    character_id: Optional[int] = Field(default=None, foreign_key="characters.id", primary_key=True)
    spell_id: Optional[int] = Field(default=None, foreign_key="spells.id", primary_key=True)

class CharacterStatLink(Base, table=True):
    character_id: Optional[int] = Field(default=None, foreign_key="characters.id", primary_key=True)
    stat_id: Optional[int] = Field(default=None, foreign_key="stats.id", primary_key=True)
    value: Optional[int] = Field(default=None)  # Store the stat value if applicable

class CharacterSkillLink(Base, table=True):
    character_id: Optional[int] = Field(default=None, foreign_key="characters.id", primary_key=True)
    skill_id: Optional[int] = Field(default=None, foreign_key="skills.id", primary_key=True)
    ranks: Optional[int] = Field(default=None)  # Track ranks in each skill

class CharacterWeaponLink(Base, table=True):
    character_id: Optional[int] = Field(default=None, foreign_key="characters.id", primary_key=True)
    weapon_id: Optional[int] = Field(default=None, foreign_key="weapons.id", primary_key=True)
    quantity: Optional[int] = Field(default=1)  # Optional: Track multiple weapons of the same type

class CharacterArmorLink(Base, table=True):
    character_id: Optional[int] = Field(default=None, foreign_key="characters.id", primary_key=True)
    armor_id: Optional[int] = Field(default=None, foreign_key="armor.id", primary_key=True)
    equipped: Optional[bool] = Field(default=False)  # Optional: Track if armor is equipped

class CharacterInventoryLink(Base, table=True):
    character_id: Optional[int] = Field(default=None, foreign_key="characters.id", primary_key=True)
    equipment_id: Optional[int] = Field(default=None, foreign_key="equipment.id", primary_key=True)
    quantity: Optional[int] = Field(default=1)  # Optional: Track quantity of inventory items

class CharacterMoneyLink(Base, table=True):
    character_id: Optional[int] = Field(default=None, foreign_key="characters.id", primary_key=True)
    money_id: Optional[int] = Field(default=None, foreign_key="money_values.id", primary_key=True)
