from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, List

class Character(SQLModel, table=True):
    __tablename__ = "character"
    
    id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    
    # Foreign key references to other tables
    character_class_id: Optional[int] = Field(default=None, foreign_key="character_classes.id")
    race_id: Optional[int] = Field(default=None, foreign_key="races.id")
    weapon_id: Optional[int] = Field(default=None, foreign_key="weapons.id")
    spell_id: Optional[int] = Field(default=None, foreign_key="spells.id")
    feat_id: Optional[int] = Field(default=None, foreign_key="feats.id")
    armor_id: Optional[int] = Field(default=None, foreign_key="armor.id")
    caster_type_id: Optional[int] = Field(default=None, foreign_key="caster_types.id")
    money_value_id: Optional[int] = Field(default=None, foreign_key="money_values.id")
    racial_trait_id: Optional[int] = Field(default=None, foreign_key="racial_traits.id")
    saving_throw_progression_id: Optional[int] = Field(default=None, foreign_key="saving_throw_progressions.id")
    skill_id: Optional[int] = Field(default=None, foreign_key="skills.id")
    stat_id: Optional[int] = Field(default=None, foreign_key="stats.id")
    class_ability_id: Optional[int] = Field(default=None, foreign_key="class_abilities.id")
    language_id: Optional[int] = Field(default=None, foreign_key="languages.id")
    bab_id: Optional[int] = Field(default=None, foreign_key="bab_progressions.id")
    equipment_id: Optional[int] = Field(default=None, foreign_key="equipment.id")
    alignment_id: Optional[int] = Field(default=None, foreign_key="alignments.id")
