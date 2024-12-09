import uvicorn
import jwt
from typing import List, Annotated
from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from db import get_session
from models import Character, Armor, CharacterArmorLink, CharacterInventoryLink, CharacterMoneyLink, CharacterSkillLink, Spell, CharacterSpellLink, CharacterStatLink, Weapon, CharacterWeaponLink, Feat, CharacterFeatLink
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from config import SUPABASE_SECRET_KEY, JWT_ALGORITHM   
from api.race_endpoints import router as race_router
from api.armor_endpoints import router as armor_router
from api.alignment_endpoints import router as alignment_router
from api.class_endpoints import router as class_router
from api.bab_endpoints import router as bab_router
from api.caster_endpoints import router as caster_router
from api.feat_endpoints import router as feat_router
from api.stat_endpoints import router as stat_router
from api.save_endpoints import router as save_router
from api.equipment_endpoints import router as equipment_router
from api.skill_endpoints import router as skill_router
from api.money_endpoints import router as money_router
from api.language_endpoints import router as language_router
from api.spell_endpoints import router as spell_router
from api.weapon_endpoints import router as weapon_router
from api.class_ability_endpoints import router as ability_router
from api.racial_trait_endpoints import router as trait_router

app = FastAPI(redirect_slashes=False)

app.include_router(ability_router, prefix="/class_abilities", tags=["Class Abilities"])
app.include_router(trait_router, prefix="/racial_traits", tags=["Racial Traits"])
app.include_router(weapon_router, prefix="/weapons", tags=["Weapons"])
app.include_router(spell_router, prefix="/spells", tags=["Spells"])
app.include_router(race_router, prefix="/races", tags=["Races"])
app.include_router(armor_router, prefix="/armor", tags=["Armor"])
app.include_router(alignment_router, prefix="/alignments", tags=["Alignments"])
app.include_router(class_router, prefix="/character_classes", tags=["Classes"])
app.include_router(bab_router, prefix="/bab_progressions", tags=["Base Attack Bonus"])
app.include_router(caster_router, prefix="/caster_types", tags=["Caster Types"])
app.include_router(feat_router, prefix="/feats", tags=["Feats"])
app.include_router(stat_router, prefix="/stats", tags=["Stats"])
app.include_router(save_router, prefix="/saving_throw_progressions", tags=["Saves"])
app.include_router(equipment_router, prefix="/equipment", tags=["Equipment"])
app.include_router(skill_router, prefix="/skills", tags=["Skills"])
app.include_router(money_router, prefix="/money_values", tags=["Money"])
app.include_router(language_router, prefix="/languages", tags=["Languages"])

origins = [
    'http://localhost',
    'http://localhost:3000',
    'http://localhost:5173',
    'https://pathforger.netlify.app'
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

# Retrieve all characters
@app.get("/characters/", response_model=List[Character])
def read_all_characters(session: Session = Depends(get_session)):
    characters = session.exec(select(Character)).all()
    return characters


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

# Retrieve all character inventory links
@app.get("/character_inventory/", response_model=List[CharacterInventoryLink])
def read_all_character_inventory(session: Session = Depends(get_session)):
    character_inventory = session.exec(select(CharacterInventoryLink)).all()
    return character_inventory

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

# Retrieve all character money links
@app.get("/character_money/", response_model=List[CharacterMoneyLink])
def read_all_character_money(session: Session = Depends(get_session)):
    character_money = session.exec(select(CharacterMoneyLink)).all()
    return character_money

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


# Retrieve all character skills links
@app.get("/character_skills/", response_model=List[CharacterSkillLink])
def read_all_character_skills(session: Session = Depends(get_session)):
    character_skills = session.exec(select(CharacterSkillLink)).all()
    return character_skills

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

# Retrieve all character spells
@app.get("/character_spells/", response_model=List[CharacterSpellLink])
def read_all_character_spells(session: Session = Depends(get_session)):
    character_spells = session.exec(select(CharacterSpellLink)).all()
    return character_spells

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

# Retrieve all character stats links
@app.get("/character_stats/", response_model=List[CharacterStatLink])
def read_all_character_stats(session: Session = Depends(get_session)):
    character_stats = session.exec(select(CharacterStatLink)).all()
    return character_stats

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

# Retrieve all character weapons
@app.get("/character_weapons/", response_model=List[CharacterWeaponLink])
def read_all_character_weapons(session: Session = Depends(get_session)):
    character_weapons = session.exec(select(CharacterWeaponLink)).all()
    return character_weapons

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
