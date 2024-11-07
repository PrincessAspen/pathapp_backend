import uvicorn
import jwt
from typing import List, Annotated
from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from db import get_session
from models import Armor, CasterType, Feat, MoneyValue, Race, RacialTrait, SavingThrowProgression, Skill, Spell, Stat, Weapon, CharacterClass, ClassAbility, Character, Language, Equipment, Alignment, BABProgression
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from config import SUPABASE_SECRET_KEY, JWT_ALGORITHM   

app = FastAPI()

origins = [
    'http://localhost',
    'http://localhost:3000',
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*']
)

@app.get("/")
def root():
    return {"message": "Hello World"}

app.mount("/images", StaticFiles(directory="images"), name="images")

# Security dependency
security = HTTPBearer()

def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SUPABASE_SECRET_KEY,
            audience=["authenticated"],
            algorithms=[JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def check_current_credentials(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    token = credentials.credentials
    payload = verify_token(token)
    return payload

@app.post("/armor/", response_model=Armor)
def create_armor(armor: Armor, session: Session = Depends(get_session)):
    session.add(armor)
    session.commit()
    session.refresh(armor)
    return armor

@app.get("/armor/{armor_id}", response_model=Armor)
def read_armor(armor_id: int, session: Session = Depends(get_session)):
    armor = session.get(Armor, armor_id)
    if not armor:
        raise HTTPException(status_code=404, detail="Armor not found")
    return armor

@app.put("/armor/{armor_id}", response_model=Armor)
def update_armor(armor_id: int, armor_update: Armor, session: Session = Depends(get_session)):
    armor = session.get(Armor, armor_id)
    if not armor:
        raise HTTPException(status_code=404, detail="Armor not found")
    
    for key, value in armor_update.dict(exclude_unset=True).items():
        setattr(armor, key, value)
    
    session.commit()
    session.refresh(armor)
    return armor

@app.delete("/armor/{armor_id}")
def delete_armor(armor_id: int, session: Session = Depends(get_session)):
    armor = session.get(Armor, armor_id)
    if not armor:
        raise HTTPException(status_code=404, detail="Armor not found")
    session.delete(armor)
    session.commit()
    return {"message": "Armor deleted successfully"}

@app.post("/caster_types/", response_model=CasterType)
def create_caster_type(caster_type: CasterType, session: Session = Depends(get_session)):
    session.add(caster_type)
    session.commit()
    session.refresh(caster_type)
    return caster_type

@app.get("/caster_types/{caster_type_id}", response_model=CasterType)
def read_caster_type(caster_type_id: int, session: Session = Depends(get_session)):
    caster_type = session.get(CasterType, caster_type_id)
    if not caster_type:
        raise HTTPException(status_code=404, detail="Caster Type not found")
    return caster_type

@app.put("/caster_types/{caster_type_id}", response_model=CasterType)
def update_caster_type(caster_type_id: int, caster_type_update: CasterType, session: Session = Depends(get_session)):
    caster_type = session.get(CasterType, caster_type_id)
    if not caster_type:
        raise HTTPException(status_code=404, detail="Caster Type not found")
    
    for key, value in caster_type_update.dict(exclude_unset=True).items():
        setattr(caster_type, key, value)
    
    session.commit()
    session.refresh(caster_type)
    return caster_type

@app.delete("/caster_types/{caster_type_id}")
def delete_caster_type(caster_type_id: int, session: Session = Depends(get_session)):
    caster_type = session.get(CasterType, caster_type_id)
    if not caster_type:
        raise HTTPException(status_code=404, detail="Caster Type not found")
    session.delete(caster_type)
    session.commit()
    return {"message": "Caster Type deleted successfully"}

@app.post("/feats/", response_model=Feat)
def create_feat(feat: Feat, session: Session = Depends(get_session)):
    session.add(feat)
    session.commit()
    session.refresh(feat)
    return feat

@app.get("/feats/{feat_id}", response_model=Feat)
def read_feat(feat_id: int, session: Session = Depends(get_session)):
    feat = session.get(Feat, feat_id)
    if not feat:
        raise HTTPException(status_code=404, detail="Feat not found")
    return feat

@app.put("/feats/{feat_id}", response_model=Feat)
def update_feat(feat_id: int, feat_update: Feat, session: Session = Depends(get_session)):
    feat = session.get(Feat, feat_id)
    if not feat:
        raise HTTPException(status_code=404, detail="Feat not found")
    
    for key, value in feat_update.dict(exclude_unset=True).items():
        setattr(feat, key, value)
    
    session.commit()
    session.refresh(feat)
    return feat

@app.delete("/feats/{feat_id}")
def delete_feat(feat_id: int, session: Session = Depends(get_session)):
    feat = session.get(Feat, feat_id)
    if not feat:
        raise HTTPException(status_code=404, detail="Feat not found")
    session.delete(feat)
    session.commit()
    return {"message": "Feat deleted successfully"}

@app.post("/money_values/", response_model=MoneyValue)
def create_money_value(money_value: MoneyValue, session: Session = Depends(get_session)):
    session.add(money_value)
    session.commit()
    session.refresh(money_value)
    return money_value

@app.get("/money_values/{money_value_id}", response_model=MoneyValue)
def read_money_value(money_value_id: int, session: Session = Depends(get_session)):
    money_value = session.get(MoneyValue, money_value_id)
    if not money_value:
        raise HTTPException(status_code=404, detail="Money Value not found")
    return money_value

@app.put("/money_values/{money_value_id}", response_model=MoneyValue)
def update_money_value(money_value_id: int, money_value_update: MoneyValue, session: Session = Depends(get_session)):
    money_value = session.get(MoneyValue, money_value_id)
    if not money_value:
        raise HTTPException(status_code=404, detail="Money Value not found")
    
    for key, value in money_value_update.dict(exclude_unset=True).items():
        setattr(money_value, key, value)
    
    session.commit()
    session.refresh(money_value)
    return money_value

@app.delete("/money_values/{money_value_id}")
def delete_money_value(money_value_id: int, session: Session = Depends(get_session)):
    money_value = session.get(MoneyValue, money_value_id)
    if not money_value:
        raise HTTPException(status_code=404, detail="Money Value not found")
    session.delete(money_value)
    session.commit()
    return {"message": "Money Value deleted successfully"}

@app.post("/races/", response_model=Race)
def create_race(race: Race, session: Session = Depends(get_session)):
    session.add(race)
    session.commit()
    session.refresh(race)
    return race

@app.get("/races/{race_id}", response_model=Race)
def read_race(race_id: int, session: Session = Depends(get_session)):
    race = session.get(Race, race_id)
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    return race

@app.put("/races/{race_id}", response_model=Race)
def update_race(race_id: int, race_update: Race, session: Session = Depends(get_session)):
    race = session.get(Race, race_id)
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    
    for key, value in race_update.dict(exclude_unset=True).items():
        setattr(race, key, value)
    
    session.commit()
    session.refresh(race)
    return race

@app.delete("/races/{race_id}")
def delete_race(race_id: int, session: Session = Depends(get_session)):
    race = session.get(Race, race_id)
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    session.delete(race)
    session.commit()
    return {"message": "Race deleted successfully"}

@app.post("/racial_traits/", response_model=RacialTrait)
def create_racial_trait(racial_trait: RacialTrait, session: Session = Depends(get_session)):
    session.add(racial_trait)
    session.commit()
    session.refresh(racial_trait)
    return racial_trait

@app.get("/racial_traits/{racial_trait_id}", response_model=RacialTrait)
def read_racial_trait(racial_trait_id: int, session: Session = Depends(get_session)):
    racial_trait = session.get(RacialTrait, racial_trait_id)
    if not racial_trait:
        raise HTTPException(status_code=404, detail="Racial Trait not found")
    return racial_trait

@app.put("/racial_traits/{racial_trait_id}", response_model=RacialTrait)
def update_racial_trait(racial_trait_id: int, racial_trait_update: RacialTrait, session: Session = Depends(get_session)):
    racial_trait = session.get(RacialTrait, racial_trait_id)
    if not racial_trait:
        raise HTTPException(status_code=404, detail="Racial Trait not found")
    
    for key, value in racial_trait_update.dict(exclude_unset=True).items():
        setattr(racial_trait, key, value)
    
    session.commit()
    session.refresh(racial_trait)
    return racial_trait

@app.delete("/racial_traits/{racial_trait_id}")
def delete_racial_trait(racial_trait_id: int, session: Session = Depends(get_session)):
    racial_trait = session.get(RacialTrait, racial_trait_id)
    if not racial_trait:
        raise HTTPException(status_code=404, detail="Racial Trait not found")
    session.delete(racial_trait)
    session.commit()
    return {"message": "Racial Trait deleted successfully"}

@app.post("/saving_throw_progressions/", response_model=SavingThrowProgression)
def create_saving_throw_progression(saving_throw_progression: SavingThrowProgression, session: Session = Depends(get_session)):
    session.add(saving_throw_progression)
    session.commit()
    session.refresh(saving_throw_progression)
    return saving_throw_progression

@app.get("/saving_throw_progressions/{progression_id}", response_model=SavingThrowProgression)
def read_saving_throw_progression(progression_id: int, session: Session = Depends(get_session)):
    saving_throw_progression = session.get(SavingThrowProgression, progression_id)
    if not saving_throw_progression:
        raise HTTPException(status_code=404, detail="Saving Throw Progression not found")
    return saving_throw_progression

@app.put("/saving_throw_progressions/{progression_id}", response_model=SavingThrowProgression)
def update_saving_throw_progression(progression_id: int, progression_update: SavingThrowProgression, session: Session = Depends(get_session)):
    saving_throw_progression = session.get(SavingThrowProgression, progression_id)
    if not saving_throw_progression:
        raise HTTPException(status_code=404, detail="Saving Throw Progression not found")
    
    for key, value in progression_update.dict(exclude_unset=True).items():
        setattr(saving_throw_progression, key, value)
    
    session.commit()
    session.refresh(saving_throw_progression)
    return saving_throw_progression

@app.delete("/saving_throw_progressions/{progression_id}")
def delete_saving_throw_progression(progression_id: int, session: Session = Depends(get_session)):
    saving_throw_progression = session.get(SavingThrowProgression, progression_id)
    if not saving_throw_progression:
        raise HTTPException(status_code=404, detail="Saving Throw Progression not found")
    session.delete(saving_throw_progression)
    session.commit()
    return {"message": "Saving Throw Progression deleted successfully"}

@app.post("/skills/", response_model=Skill)
def create_skill(skill: Skill, session: Session = Depends(get_session)):
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill

@app.get("/skills/{skill_id}", response_model=Skill)
def read_skill(skill_id: int, session: Session = Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@app.put("/skills/{skill_id}", response_model=Skill)
def update_skill(skill_id: int, skill_update: Skill, session: Session = Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    for key, value in skill_update.dict(exclude_unset=True).items():
        setattr(skill, key, value)
    
    session.commit()
    session.refresh(skill)
    return skill

@app.delete("/skills/{skill_id}")
def delete_skill(skill_id: int, session: Session = Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    session.delete(skill)
    session.commit()
    return {"message": "Skill deleted successfully"}

@app.post("/spells/", response_model=Spell)
def create_spell(spell: Spell, session: Session = Depends(get_session)):
    session.add(spell)
    session.commit()
    session.refresh(spell)
    return spell

@app.get("/spells/{spell_id}", response_model=Spell)
def read_spell(spell_id: int, session: Session = Depends(get_session)):
    spell = session.get(Spell, spell_id)
    if not spell:
        raise HTTPException(status_code=404, detail="Spell not found")
    return spell

@app.put("/spells/{spell_id}", response_model=Spell)
def update_spell(spell_id: int, spell_update: Spell, session: Session = Depends(get_session)):
    spell = session.get(Spell, spell_id)
    if not spell:
        raise HTTPException(status_code=404, detail="Spell not found")
    
    for key, value in spell_update.dict(exclude_unset=True).items():
        setattr(spell, key, value)
    
    session.commit()
    session.refresh(spell)
    return spell

@app.delete("/spells/{spell_id}")
def delete_spell(spell_id: int, session: Session = Depends(get_session)):
    spell = session.get(Spell, spell_id)
    if not spell:
        raise HTTPException(status_code=404, detail="Spell not found")
    session.delete(spell)
    session.commit()
    return {"message": "Spell deleted successfully"}

@app.post("/stats/", response_model=Stat)
def create_stat(stat: Stat, session: Session = Depends(get_session)):
    session.add(stat)
    session.commit()
    session.refresh(stat)
    return stat

@app.get("/stats/{stat_id}", response_model=Stat)
def read_stat(stat_id: int, session: Session = Depends(get_session)):
    stat = session.get(Stat, stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="Stat not found")
    return stat

@app.put("/stats/{stat_id}", response_model=Stat)
def update_stat(stat_id: int, stat_update: Stat, session: Session = Depends(get_session)):
    stat = session.get(Stat, stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="Stat not found")
    
    for key, value in stat_update.dict(exclude_unset=True).items():
        setattr(stat, key, value)
    
    session.commit()
    session.refresh(stat)
    return stat

@app.delete("/stats/{stat_id}")
def delete_stat(stat_id: int, session: Session = Depends(get_session)):
    stat = session.get(Stat, stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="Stat not found")
    session.delete(stat)
    session.commit()
    return {"message": "Stat deleted successfully"}

@app.post("/weapons/", response_model=Weapon)
def create_weapon(weapon: Weapon, session: Session = Depends(get_session)):
    session.add(weapon)
    session.commit()
    session.refresh(weapon)
    return weapon

@app.get("/weapons/{weapon_id}", response_model=Weapon)
def read_weapon(weapon_id: int, session: Session = Depends(get_session)):
    weapon = session.get(Weapon, weapon_id)
    if not weapon:
        raise HTTPException(status_code=404, detail="Weapon not found")
    return weapon

@app.put("/weapons/{weapon_id}", response_model=Weapon)
def update_weapon(weapon_id: int, weapon_update: Weapon, session: Session = Depends(get_session)):
    weapon = session.get(Weapon, weapon_id)
    if not weapon:
        raise HTTPException(status_code=404, detail="Weapon not found")
    
    for key, value in weapon_update.dict(exclude_unset=True).items():
        setattr(weapon, key, value)
    
    session.commit()
    session.refresh(weapon)
    return weapon

@app.delete("/weapons/{weapon_id}")
def delete_weapon(weapon_id: int, session: Session = Depends(get_session)):
    weapon = session.get(Weapon, weapon_id)
    if not weapon:
        raise HTTPException(status_code=404, detail="Weapon not found")
    session.delete(weapon)
    session.commit()
    return {"message": "Weapon deleted successfully"}


# CharacterClass CRUD Operations

@app.post("/create/character_class")
def create_character_class(
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    hit_die: Annotated[int, Form()],
    base_attack_bonus: Annotated[str, Form()],  # Changed to str to parse as JSON
    saving_throws: Annotated[str, Form()],  # Changed to str to parse as JSON
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Session = Depends(get_session)
):
    token = credentials.credentials
    is_valid = verify_token(token)
    
    if not is_valid:
        raise HTTPException(status_code=403, detail="Not Authorized")
    
    # Parse base_attack_bonus and saving_throws as JSON
    import json
    try:
        base_attack_bonus = json.loads(base_attack_bonus)
        saving_throws = json.loads(saving_throws)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format for base_attack_bonus or saving_throws")
    
    character_class = CharacterClass(
        name=name,
        description=description,
        hit_die=hit_die,
        base_attack_bonus=base_attack_bonus,
        saving_throws=saving_throws
    )
    session.add(character_class)
    session.commit()
    session.refresh(character_class)
    return {"character_class": character_class}

@app.get("/classes/", response_model=List[CharacterClass])
def read_character_classes(session: Session = Depends(get_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    is_valid = verify_token(token)
    
    if not is_valid:
        raise HTTPException(status_code=403, detail="Not Authorized")
    
    classes = session.exec(select(CharacterClass)).all()
    return classes

@app.post("/character_classes/", response_model=CharacterClass)
def create_character_class(character_class: CharacterClass, session: Session = Depends(get_session)):
    session.add(character_class)
    session.commit()
    session.refresh(character_class)
    return character_class

@app.get("/character_classes/{character_class_id}", response_model=CharacterClass)
def read_character_class(character_class_id: int, session: Session = Depends(get_session)):
    character_class = session.get(CharacterClass, character_class_id)
    if not character_class:
        raise HTTPException(status_code=404, detail="Character Class not found")
    return character_class

@app.put("/character_classes/{character_class_id}", response_model=CharacterClass)
def update_character_class(character_class_id: int, character_class_update: CharacterClass, session: Session = Depends(get_session)):
    character_class = session.get(CharacterClass, character_class_id)
    if not character_class:
        raise HTTPException(status_code=404, detail="Character Class not found")
    
    for key, value in character_class_update.dict(exclude_unset=True).items():
        setattr(character_class, key, value)
    
    session.commit()
    session.refresh(character_class)
    return character_class

@app.delete("/character_classes/{character_class_id}")
def delete_character_class(character_class_id: int, session: Session = Depends(get_session)):
    character_class = session.get(CharacterClass, character_class_id)
    if not character_class:
        raise HTTPException(status_code=404, detail="Character Class not found")
    session.delete(character_class)
    session.commit()
    return {"message": "Character Class deleted successfully"}

@app.post("/class_abilities/", response_model=ClassAbility)
def create_class_ability(class_ability: ClassAbility, session: Session = Depends(get_session)):
    session.add(class_ability)
    session.commit()
    session.refresh(class_ability)
    return class_ability

@app.get("/class_abilities/{ability_id}", response_model=ClassAbility)
def read_class_ability(ability_id: int, session: Session = Depends(get_session)):
    class_ability = session.get(ClassAbility, ability_id)
    if not class_ability:
        raise HTTPException(status_code=404, detail="Class Ability not found")
    return class_ability

@app.put("/class_abilities/{ability_id}", response_model=ClassAbility)
def update_class_ability(ability_id: int, ability_update: ClassAbility, session: Session = Depends(get_session)):
    class_ability = session.get(ClassAbility, ability_id)
    if not class_ability:
        raise HTTPException(status_code=404, detail="Class Ability not found")
    
    for key, value in ability_update.dict(exclude_unset=True).items():
        setattr(class_ability, key, value)
    
    session.commit()
    session.refresh(class_ability)
    return class_ability

@app.delete("/class_abilities/{ability_id}")
def delete_class_ability(ability_id: int, session: Session = Depends(get_session)):
    class_ability = session.get(ClassAbility, ability_id)
    if not class_ability:
        raise HTTPException(status_code=404, detail="Class Ability not found")
    session.delete(class_ability)
    session.commit()
    return {"message": "Class Ability deleted successfully"}

@app.post("/alignments/", response_model=Alignment)
def create_alignment(alignment: Alignment, session: Session = Depends(get_session)):
    session.add(alignment)
    session.commit()
    session.refresh(alignment)
    return alignment

@app.get("/alignments/{alignment_id}", response_model=Alignment)
def read_alignment(alignment_id: int, session: Session = Depends(get_session)):
    alignment = session.get(Alignment, alignment_id)
    if not alignment:
        raise HTTPException(status_code=404, detail="Alignment not found")
    return alignment

@app.put("/alignments/{alignment_id}", response_model=Alignment)
def update_alignment(alignment_id: int, alignment_update: Alignment, session: Session = Depends(get_session)):
    alignment = session.get(Alignment, alignment_id)
    if not alignment:
        raise HTTPException(status_code=404, detail="Alignment not found")
    
    for key, value in alignment_update.dict(exclude_unset=True).items():
        setattr(alignment, key, value)
    
    session.commit()
    session.refresh(alignment)
    return alignment

@app.delete("/alignments/{alignment_id}")
def delete_alignment(alignment_id: int, session: Session = Depends(get_session)):
    alignment = session.get(Alignment, alignment_id)
    if not alignment:
        raise HTTPException(status_code=404, detail="Alignment not found")
    session.delete(alignment)
    session.commit()
    return {"message": "Alignment deleted successfully"}


@app.post("/bab_progressions/", response_model=BABProgression)
def create_bab_progression(bab_progression: BABProgression, session: Session = Depends(get_session)):
    session.add(bab_progression)
    session.commit()
    session.refresh(bab_progression)
    return bab_progression

@app.get("/bab_progressions/{bab_progression_id}", response_model=BABProgression)
def read_bab_progression(bab_progression_id: int, session: Session = Depends(get_session)):
    bab_progression = session.get(BABProgression, bab_progression_id)
    if not bab_progression:
        raise HTTPException(status_code=404, detail="BAB Progression not found")
    return bab_progression

@app.put("/bab_progressions/{bab_progression_id}", response_model=BABProgression)
def update_bab_progression(bab_progression_id: int, bab_progression_update: BABProgression, session: Session = Depends(get_session)):
    bab_progression = session.get(BABProgression, bab_progression_id)
    if not bab_progression:
        raise HTTPException(status_code=404, detail="BAB Progression not found")
    
    for key, value in bab_progression_update.dict(exclude_unset=True).items():
        setattr(bab_progression, key, value)
    
    session.commit()
    session.refresh(bab_progression)
    return bab_progression

@app.delete("/bab_progressions/{bab_progression_id}")
def delete_bab_progression(bab_progression_id: int, session: Session = Depends(get_session)):
    bab_progression = session.get(BABProgression, bab_progression_id)
    if not bab_progression:
        raise HTTPException(status_code=404, detail="BAB Progression not found")
    session.delete(bab_progression)
    session.commit()
    return {"message": "BAB Progression deleted successfully"}


@app.post("/equipment/", response_model=Equipment)
def create_equipment(equipment: Equipment, session: Session = Depends(get_session)):
    session.add(equipment)
    session.commit()
    session.refresh(equipment)
    return equipment

@app.get("/equipment/{equipment_id}", response_model=Equipment)
def read_equipment(equipment_id: int, session: Session = Depends(get_session)):
    equipment = session.get(Equipment, equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@app.put("/equipment/{equipment_id}", response_model=Equipment)
def update_equipment(equipment_id: int, equipment_update: Equipment, session: Session = Depends(get_session)):
    equipment = session.get(Equipment, equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    for key, value in equipment_update.dict(exclude_unset=True).items():
        setattr(equipment, key, value)
    
    session.commit()
    session.refresh(equipment)
    return equipment

@app.delete("/equipment/{equipment_id}")
def delete_equipment(equipment_id: int, session: Session = Depends(get_session)):
    equipment = session.get(Equipment, equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    session.delete(equipment)
    session.commit()
    return {"message": "Equipment deleted successfully"}


@app.post("/languages/", response_model=Language)
def create_language(language: Language, session: Session = Depends(get_session)):
    session.add(language)
    session.commit()
    session.refresh(language)
    return language

@app.get("/languages/{language_id}", response_model=Language)
def read_language(language_id: int, session: Session = Depends(get_session)):
    language = session.get(Language, language_id)
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    return language

@app.put("/languages/{language_id}", response_model=Language)
def update_language(language_id: int, language_update: Language, session: Session = Depends(get_session)):
    language = session.get(Language, language_id)
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    
    for key, value in language_update.dict(exclude_unset=True).items():
        setattr(language, key, value)
    
    session.commit()
    session.refresh(language)
    return language

@app.delete("/languages/{language_id}")
def delete_language(language_id: int, session: Session = Depends(get_session)):
    language = session.get(Language, language_id)
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    session.delete(language)
    session.commit()
    return {"message": "Language deleted successfully"}


@app.post("/characters/", response_model=Character)
def create_character(character: Character, session: Session = Depends(get_session)):
    session.add(character)
    session.commit()
    session.refresh(character)
    return character

@app.get("/characters/{character_id}", response_model=Character)
def read_character(character_id: int, session: Session = Depends(get_session)):
    character = session.exec(select(Character).where(Character.id == character_id)).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@app.put("/characters/{character_id}", response_model=Character)
def update_character(character_id: int, character_update: Character, session: Session = Depends(get_session)):
    character = session.get(Character, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    for key, value in character_update.dict(exclude_unset=True).items():
        setattr(character, key, value)
    
    session.commit()
    session.refresh(character)
    return character

@app.delete("/characters/{character_id}")
def delete_character(character_id: int, session: Session = Depends(get_session)):
    character = session.get(Character, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    session.delete(character)
    session.commit()
    return {"message": "Character deleted successfully"}



if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
