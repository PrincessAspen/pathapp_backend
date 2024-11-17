import uvicorn
import jwt
from typing import List, Annotated
from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from db import get_session
from models import Armor, CasterType, Feat, MoneyValue, Race, RacialTrait, SavingThrowProgression, Skill, Spell, Stat, Weapon, CharacterClass, ClassAbility, Character, Language, Equipment, Alignment, BABProgression, CharacterWeaponLink, CharacterArmorLink, CharacterFeatLink, CharacterInventoryLink, CharacterMoneyLink, CharacterSkillLink, CharacterSpellLink, CharacterStatLink
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

@app.get("/characters/")
def get_characters(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], session: Session = Depends(get_session)):
    payload = check_current_credentials(credentials)  # Get user info from the token
    user_id = payload["sub"]  # Extract the `sub` from the JWT payload, which is the user's `uid`

    # Query the characters for the authenticated user (user_id)
    characters = session.exec(select(Character).where(Character.user_id == user_id)).all()

    return characters

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

@app.get("/alignments/", response_model=List[Alignment])
def read_alignments(session: Session = Depends(get_session)):
    alignments = session.exec(select(Alignment)).all()
    if not alignments:
        raise HTTPException(status_code=404, detail="No alignments found")
    return alignments

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


@app.post("/characters/")
def create_character(character: Character, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], session: Session = Depends(get_session)):
    payload = check_current_credentials(credentials)  # Get user info from the token
    user_id = payload["sub"]  # Extract user_id from the token
    
    # Assign the user_id to the character
    character.user_id = user_id  # Link the character with the authenticated user
    
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
def update_character(
    character_id: int,
    character_update: Character,  # The updated character data will be provided in the request body
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Session = Depends(get_session)
):
    payload = check_current_credentials(credentials)  # Get user info from the token
    user_id = payload["sub"]  # Extract the `sub` (user ID) from the JWT payload

    # Retrieve the character by its ID
    character = session.get(Character, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    # Ensure the character belongs to the authenticated user
    if character.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can only update your own characters")

    # Update the character's fields
    for key, value in character_update.dict(exclude_unset=True).items():
        setattr(character, key, value)

    session.commit()
    session.refresh(character)
    return character


@app.delete("/characters/{character_id}")
def delete_character(
    character_id: int,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Session = Depends(get_session)
):
    payload = check_current_credentials(credentials)  # Get user info from the token
    user_id = payload["sub"]  # Extract the `sub` (user ID) from the JWT payload

    # Retrieve the character by its ID
    character = session.get(Character, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    # Ensure the character belongs to the authenticated user
    if character.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can only delete your own characters")

    # Delete the character
    session.delete(character)
    session.commit()
    return {"message": "Character deleted successfully"}


# Create a link between a character and a spell
@app.post("/character_spells/", response_model=CharacterSpellLink)
def create_character_spell_link(character_id: int, spell_id: int, session: Session = Depends(get_session)):
    # Verify both character and spell exist
    character = session.get(Character, character_id)
    spell = session.get(Spell, spell_id)
    if not character or not spell:
        raise HTTPException(status_code=404, detail="Character or Spell not found")
    
    # Create the link
    character_spell_link = CharacterSpellLink(character_id=character_id, spell_id=spell_id)
    session.add(character_spell_link)
    session.commit()
    session.refresh(character_spell_link)
    return character_spell_link

# Get all spells for a specific character
@app.get("/character_spells/{character_id}", response_model=List[Spell])
def get_spells_for_character(character_id: int, session: Session = Depends(get_session)):
    character = session.get(Character, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    # Query to retrieve all spells linked to this character
    spells = session.exec(
        select(Spell).join(CharacterSpellLink).where(CharacterSpellLink.character_id == character_id)
    ).all()
    return spells

# Update a character's spell link (changing a spell for a character)
@app.put("/character_spells/{character_spell_link_id}", response_model=CharacterSpellLink)
def update_character_spell_link(character_spell_link_id: int, new_spell_id: int, session: Session = Depends(get_session)):
    link = session.get(CharacterSpellLink, character_spell_link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Character-Spell Link not found")
    
    new_spell = session.get(Spell, new_spell_id)
    if not new_spell:
        raise HTTPException(status_code=404, detail="New Spell not found")

    # Update the link
    link.spell_id = new_spell_id
    session.commit()
    session.refresh(link)
    return link

# Delete a character's spell link
@app.delete("/character_spells/{character_spell_link_id}")
def delete_character_spell_link(character_spell_link_id: int, session: Session = Depends(get_session)):
    link = session.get(CharacterSpellLink, character_spell_link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Character-Spell Link not found")
    
    session.delete(link)
    session.commit()
    return {"message": "Character-Spell link deleted successfully"}

# Create a link between a character and a feat
@app.post("/character_feats/", response_model=CharacterFeatLink)
def create_character_feat_link(character_id: int, feat_id: int, session: Session = Depends(get_session)):
    character = session.get(Character, character_id)
    feat = session.get(Feat, feat_id)
    if not character or not feat:
        raise HTTPException(status_code=404, detail="Character or Feat not found")

    character_feat_link = CharacterFeatLink(character_id=character_id, feat_id=feat_id)
    session.add(character_feat_link)
    session.commit()
    session.refresh(character_feat_link)
    return character_feat_link

# Get all feats for a specific character
@app.get("/character_feats/{character_id}", response_model=List[Feat])
def get_feats_for_character(character_id: int, session: Session = Depends(get_session)):
    feats = session.exec(
        select(Feat).join(CharacterFeatLink).where(CharacterFeatLink.character_id == character_id)
    ).all()
    return feats

# Update a character’s feat link
@app.put("/character_feats/{character_feat_link_id}", response_model=CharacterFeatLink)
def update_character_feat_link(character_feat_link_id: int, new_feat_id: int, session: Session = Depends(get_session)):
    link = session.get(CharacterFeatLink, character_feat_link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Character-Feat Link not found")
    
    link.feat_id = new_feat_id
    session.commit()
    session.refresh(link)
    return link

# Delete a character’s feat link
@app.delete("/character_feats/{character_feat_link_id}")
def delete_character_feat_link(character_feat_link_id: int, session: Session = Depends(get_session)):
    link = session.get(CharacterFeatLink, character_feat_link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Character-Feat Link not found")
    
    session.delete(link)
    session.commit()
    return {"message": "Character-Feat link deleted successfully"}

# Create a link between a character and a weapon
@app.post("/character_weapons/", response_model=CharacterWeaponLink)
def create_character_weapon_link(character_id: int, weapon_id: int, session: Session = Depends(get_session)):
    character = session.get(Character, character_id)
    weapon = session.get(Weapon, weapon_id)
    if not character or not weapon:
        raise HTTPException(status_code=404, detail="Character or Weapon not found")

    character_weapon_link = CharacterWeaponLink(character_id=character_id, weapon_id=weapon_id)
    session.add(character_weapon_link)
    session.commit()
    session.refresh(character_weapon_link)
    return character_weapon_link

# Get all weapons for a specific character
@app.get("/character_weapons/{character_id}", response_model=List[Weapon])
def get_weapons_for_character(character_id: int, session: Session = Depends(get_session)):
    weapons = session.exec(
        select(Weapon).join(CharacterWeaponLink).where(CharacterWeaponLink.character_id == character_id)
    ).all()
    return weapons

# Update a character’s weapon link
@app.put("/character_weapons/{character_weapon_link_id}", response_model=CharacterWeaponLink)
def update_character_weapon_link(character_weapon_link_id: int, new_weapon_id: int, session: Session = Depends(get_session)):
    link = session.get(CharacterWeaponLink, character_weapon_link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Character-Weapon Link not found")
    
    link.weapon_id = new_weapon_id
    session.commit()
    session.refresh(link)
    return link

# Delete a character’s weapon link
@app.delete("/character_weapons/{character_weapon_link_id}")
def delete_character_weapon_link(character_weapon_link_id: int, session: Session = Depends(get_session)):
    link = session.get(CharacterWeaponLink, character_weapon_link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Character-Weapon Link not found")
    
    session.delete(link)
    session.commit()
    return {"message": "Character-Weapon link deleted successfully"}

# Create a link between a character and an armor
@app.post("/character_armors/", response_model=CharacterArmorLink)
def create_character_armor_link(character_id: int, armor_id: int, session: Session = Depends(get_session)):
    character = session.get(Character, character_id)
    armor = session.get(Armor, armor_id)
    if not character or not armor:
        raise HTTPException(status_code=404, detail="Character or Armor not found")

    character_armor_link = CharacterArmorLink(character_id=character_id, armor_id=armor_id)
    session.add(character_armor_link)
    session.commit()
    session.refresh(character_armor_link)
    return character_armor_link

# Get all armor for a specific character
@app.get("/character_armors/{character_id}", response_model=List[Armor])
def get_armor_for_character(character_id: int, session: Session = Depends(get_session)):
    armors = session.exec(
        select(Armor).join(CharacterArmorLink).where(CharacterArmorLink.character_id == character_id)
    ).all()
    return armors

# Update a character’s armor link
@app.put("/character_armors/{character_armor_link_id}", response_model=CharacterArmorLink)
def update_character_armor_link(character_armor_link_id: int, new_armor_id: int, session: Session = Depends(get_session)):
    link = session.get(CharacterArmorLink, character_armor_link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Character-Armor Link not found")
    
    link.armor_id = new_armor_id
    session.commit()
    session.refresh(link)
    return link

# Delete a character’s armor link
@app.delete("/character_armors/{character_armor_link_id}")
def delete_character_armor_link(character_armor_link_id: int, session: Session = Depends(get_session)):
    link = session.get(CharacterArmorLink, character_armor_link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Character-Armor Link not found")
    
    session.delete(link)
    session.commit()
    return {"message": "Character-Armor link deleted successfully"}

@app.post("/character_money/", response_model=CharacterMoneyLink)
def create_character_money_link(character_money_link: CharacterMoneyLink, session: Session = Depends(get_session)):
    session.add(character_money_link)
    session.commit()
    session.refresh(character_money_link)
    return character_money_link

@app.get("/character_money/{character_id}", response_model=List[CharacterMoneyLink])
def read_character_money_links(character_id: int, session: Session = Depends(get_session)):
    money_links = session.exec(select(CharacterMoneyLink).where(CharacterMoneyLink.character_id == character_id)).all()
    return money_links

@app.put("/character_money/{character_id}/{money_id}", response_model=CharacterMoneyLink)
def update_character_money_link(character_id: int, money_id: int, money_link_update: CharacterMoneyLink, session: Session = Depends(get_session)):
    money_link = session.get(CharacterMoneyLink, (character_id, money_id))
    if not money_link:
        raise HTTPException(status_code=404, detail="Money link not found")
    for key, value in money_link_update.dict(exclude_unset=True).items():
        setattr(money_link, key, value)
    session.commit()
    session.refresh(money_link)
    return money_link

@app.delete("/character_money/{character_id}/{money_id}")
def delete_character_money_link(character_id: int, money_id: int, session: Session = Depends(get_session)):
    money_link = session.get(CharacterMoneyLink, (character_id, money_id))
    if not money_link:
        raise HTTPException(status_code=404, detail="Money link not found")
    session.delete(money_link)
    session.commit()
    return {"message": "Money link deleted successfully"}

#CRUD for character stat link

@app.post("/character_stats/", response_model=CharacterStatLink)
def create_character_stat_link(character_stat_link: CharacterStatLink, session: Session = Depends(get_session)):
    session.add(character_stat_link)
    session.commit()
    session.refresh(character_stat_link)
    return character_stat_link

@app.get("/character_stats/{character_id}", response_model=List[CharacterStatLink])
def read_character_stat_links(character_id: int, session: Session = Depends(get_session)):
    stat_links = session.exec(select(CharacterStatLink).where(CharacterStatLink.character_id == character_id)).all()
    return stat_links

@app.put("/character_stats/{character_id}/{stat_id}", response_model=CharacterStatLink)
def update_character_stat_link(character_id: int, stat_id: int, stat_link_update: CharacterStatLink, session: Session = Depends(get_session)):
    stat_link = session.get(CharacterStatLink, (character_id, stat_id))
    if not stat_link:
        raise HTTPException(status_code=404, detail="Stat link not found")
    for key, value in stat_link_update.dict(exclude_unset=True).items():
        setattr(stat_link, key, value)
    session.commit()
    session.refresh(stat_link)
    return stat_link

@app.delete("/character_stats/{character_id}/{stat_id}")
def delete_character_stat_link(character_id: int, stat_id: int, session: Session = Depends(get_session)):
    stat_link = session.get(CharacterStatLink, (character_id, stat_id))
    if not stat_link:
        raise HTTPException(status_code=404, detail="Stat link not found")
    session.delete(stat_link)
    session.commit()
    return {"message": "Stat link deleted successfully"}

# CRUD for character skill link

@app.post("/character_skills/", response_model=CharacterSkillLink)
def create_character_skill_link(character_skill_link: CharacterSkillLink, session: Session = Depends(get_session)):
    session.add(character_skill_link)
    session.commit()
    session.refresh(character_skill_link)
    return character_skill_link

@app.get("/character_skills/{character_id}", response_model=List[CharacterSkillLink])
def read_character_skill_links(character_id: int, session: Session = Depends(get_session)):
    skill_links = session.exec(select(CharacterSkillLink).where(CharacterSkillLink.character_id == character_id)).all()
    return skill_links

@app.put("/character_skills/{character_id}/{skill_id}", response_model=CharacterSkillLink)
def update_character_skill_link(character_id: int, skill_id: int, skill_link_update: CharacterSkillLink, session: Session = Depends(get_session)):
    skill_link = session.get(CharacterSkillLink, (character_id, skill_id))
    if not skill_link:
        raise HTTPException(status_code=404, detail="Skill link not found")
    for key, value in skill_link_update.dict(exclude_unset=True).items():
        setattr(skill_link, key, value)
    session.commit()
    session.refresh(skill_link)
    return skill_link

@app.delete("/character_skills/{character_id}/{skill_id}")
def delete_character_skill_link(character_id: int, skill_id: int, session: Session = Depends(get_session)):
    skill_link = session.get(CharacterSkillLink, (character_id, skill_id))
    if not skill_link:
        raise HTTPException(status_code=404, detail="Skill link not found")
    session.delete(skill_link)
    session.commit()
    return {"message": "Skill link deleted successfully"}

# CRUD for character inventory link

@app.post("/character_inventory/", response_model=CharacterInventoryLink)
def create_character_inventory_link(character_inventory_link: CharacterInventoryLink, session: Session = Depends(get_session)):
    session.add(character_inventory_link)
    session.commit()
    session.refresh(character_inventory_link)
    return character_inventory_link

@app.get("/character_inventory/{character_id}", response_model=List[CharacterInventoryLink])
def read_character_inventory_links(character_id: int, session: Session = Depends(get_session)):
    inventory_links = session.exec(select(CharacterInventoryLink).where(CharacterInventoryLink.character_id == character_id)).all()
    return inventory_links

@app.put("/character_inventory/{character_id}/{equipment_id}", response_model=CharacterInventoryLink)
def update_character_inventory_link(character_id: int, equipment_id: int, inventory_link_update: CharacterInventoryLink, session: Session = Depends(get_session)):
    inventory_link = session.get(CharacterInventoryLink, (character_id, equipment_id))
    if not inventory_link:
        raise HTTPException(status_code=404, detail="Inventory link not found")
    for key, value in inventory_link_update.dict(exclude_unset=True).items():
        setattr(inventory_link, key, value)
    session.commit()
    session.refresh(inventory_link)
    return inventory_link

@app.delete("/character_inventory/{character_id}/{equipment_id}")
def delete_character_inventory_link(character_id: int, equipment_id: int, session: Session = Depends(get_session)):
    inventory_link = session.get(CharacterInventoryLink, (character_id, equipment_id))
    if not inventory_link:
        raise HTTPException(status_code=404, detail="Inventory link not found")
    session.delete(inventory_link)
    session.commit()
    return {"message": "Inventory link deleted successfully"}

# Retrieve all armors
@app.get("/armor/", response_model=List[Armor])
def read_all_armor(session: Session = Depends(get_session)):
    armors = session.exec(select(Armor)).all()
    return armors

# Retrieve all caster types
@app.get("/caster_types/", response_model=List[CasterType])
def read_all_caster_types(session: Session = Depends(get_session)):
    caster_types = session.exec(select(CasterType)).all()
    return caster_types

# Retrieve all feats
@app.get("/feats/", response_model=List[Feat])
def read_all_feats(session: Session = Depends(get_session)):
    feats = session.exec(select(Feat)).all()
    return feats

# Retrieve all money values
@app.get("/money_values/", response_model=List[MoneyValue])
def read_all_money_values(session: Session = Depends(get_session)):
    money_values = session.exec(select(MoneyValue)).all()
    return money_values

# Retrieve all races
@app.get("/races/", response_model=List[Race])
def read_all_races(session: Session = Depends(get_session)):
    races = session.exec(select(Race)).all()
    return races

# Retrieve all racial traits
@app.get("/racial_traits/", response_model=List[RacialTrait])
def read_all_racial_traits(session: Session = Depends(get_session)):
    racial_traits = session.exec(select(RacialTrait)).all()
    return racial_traits

# Retrieve all saving throw progressions
@app.get("/saving_throw_progressions/", response_model=List[SavingThrowProgression])
def read_all_saving_throw_progressions(session: Session = Depends(get_session)):
    saving_throw_progressions = session.exec(select(SavingThrowProgression)).all()
    return saving_throw_progressions

# Retrieve all skills
@app.get("/skills/", response_model=List[Skill])
def read_all_skills(session: Session = Depends(get_session)):
    skills = session.exec(select(Skill)).all()
    return skills

# Retrieve all spells
@app.get("/spells/", response_model=List[Spell])
def read_all_spells(session: Session = Depends(get_session)):
    spells = session.exec(select(Spell)).all()
    return spells

# Retrieve all stats
@app.get("/stats/", response_model=List[Stat])
def read_all_stats(session: Session = Depends(get_session)):
    stats = session.exec(select(Stat)).all()
    return stats

# Retrieve all weapons
@app.get("/weapons/", response_model=List[Weapon])
def read_all_weapons(session: Session = Depends(get_session)):
    weapons = session.exec(select(Weapon)).all()
    return weapons

# Retrieve all character classes
@app.get("/character_classes/", response_model=List[CharacterClass])
def read_all_character_classes(session: Session = Depends(get_session)):
    character_classes = session.exec(select(CharacterClass)).all()
    return character_classes

# Retrieve all class abilities
@app.get("/class_abilities/", response_model=List[ClassAbility])
def read_all_class_abilities(session: Session = Depends(get_session)):
    class_abilities = session.exec(select(ClassAbility)).all()
    return class_abilities

# Retrieve all alignments
@app.get("/alignments/", response_model=List[Alignment])
def read_all_alignments(session: Session = Depends(get_session)):
    alignments = session.exec(select(Alignment)).all()
    return alignments

# Retrieve all BAB progressions
@app.get("/bab_progressions/", response_model=List[BABProgression])
def read_all_bab_progressions(session: Session = Depends(get_session)):
    bab_progressions = session.exec(select(BABProgression)).all()
    return bab_progressions

# Retrieve all equipment
@app.get("/equipment/", response_model=List[Equipment])
def read_all_equipment(session: Session = Depends(get_session)):
    equipment = session.exec(select(Equipment)).all()
    return equipment

# Retrieve all languages
@app.get("/languages/", response_model=List[Language])
def read_all_languages(session: Session = Depends(get_session)):
    languages = session.exec(select(Language)).all()
    return languages

# Retrieve all characters
@app.get("/characters/", response_model=List[Character])
def read_all_characters(session: Session = Depends(get_session)):
    characters = session.exec(select(Character)).all()
    return characters

# Retrieve all character spells
@app.get("/character_spells/", response_model=List[CharacterSpellLink])
def read_all_character_spells(session: Session = Depends(get_session)):
    character_spells = session.exec(select(CharacterSpellLink)).all()
    return character_spells

# Retrieve all character feats
@app.get("/character_feats/", response_model=List[CharacterFeatLink])
def read_all_character_feats(session: Session = Depends(get_session)):
    character_feats = session.exec(select(CharacterFeatLink)).all()
    return character_feats

# Retrieve all character weapons
@app.get("/character_weapons/", response_model=List[CharacterWeaponLink])
def read_all_character_weapons(session: Session = Depends(get_session)):
    character_weapons = session.exec(select(CharacterWeaponLink)).all()
    return character_weapons

# Retrieve all character armors
@app.get("/character_armors/", response_model=List[CharacterArmorLink])
def read_all_character_armors(session: Session = Depends(get_session)):
    character_armors = session.exec(select(CharacterArmorLink)).all()
    return character_armors

# Retrieve all character money links
@app.get("/character_money/", response_model=List[CharacterMoneyLink])
def read_all_character_money(session: Session = Depends(get_session)):
    character_money = session.exec(select(CharacterMoneyLink)).all()
    return character_money

# Retrieve all character stats links
@app.get("/character_stats/", response_model=List[CharacterStatLink])
def read_all_character_stats(session: Session = Depends(get_session)):
    character_stats = session.exec(select(CharacterStatLink)).all()
    return character_stats

# Retrieve all character skills links
@app.get("/character_skills/", response_model=List[CharacterSkillLink])
def read_all_character_skills(session: Session = Depends(get_session)):
    character_skills = session.exec(select(CharacterSkillLink)).all()
    return character_skills

# Retrieve all character inventory links
@app.get("/character_inventory/", response_model=List[CharacterInventoryLink])
def read_all_character_inventory(session: Session = Depends(get_session)):
    character_inventory = session.exec(select(CharacterInventoryLink)).all()
    return character_inventory


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
