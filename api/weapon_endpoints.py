from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Weapon, Character, CharacterWeaponLink
from typing import List

router = APIRouter()

@router.post("/weapons/", response_model=Weapon)
def create_weapon(weapon: Weapon, session: Session = Depends(get_session)):
    session.add(weapon)
    session.commit()
    session.refresh(weapon)
    return weapon

@router.get("/weapons/{weapon_id}", response_model=Weapon)
def read_weapon(weapon_id: int, session: Session = Depends(get_session)):
    weapon = session.get(Weapon, weapon_id)
    if not weapon:
        raise HTTPException(status_code=404, detail="Weapon not found")
    return weapon

@router.put("/weapons/{weapon_id}", response_model=Weapon)
def update_weapon(weapon_id: int, weapon_update: Weapon, session: Session = Depends(get_session)):
    weapon = session.get(Weapon, weapon_id)
    if not weapon:
        raise HTTPException(status_code=404, detail="Weapon not found")
    
    for key, value in weapon_update.dict(exclude_unset=True).items():
        setattr(weapon, key, value)
    
    session.commit()
    session.refresh(weapon)
    return weapon

@router.delete("/weapons/{weapon_id}")
def delete_weapon(weapon_id: int, session: Session = Depends(get_session)):
    weapon = session.get(Weapon, weapon_id)
    if not weapon:
        raise HTTPException(status_code=404, detail="Weapon not found")
    session.delete(weapon)
    session.commit()
    return {"message": "Weapon deleted successfully"}

# Create a link between a character and a weapon
@router.post("/character_weapons/", response_model=CharacterWeaponLink)
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
@router.get("/character_weapons/{character_id}", response_model=List[Weapon])
def get_weapons_for_character(character_id: int, session: Session = Depends(get_session)):
    weapons = session.exec(
        select(Weapon).join(CharacterWeaponLink).where(CharacterWeaponLink.character_id == character_id)
    ).all()
    return weapons

# Update a character’s weapon link
@router.put("/character_weapons/{character_weapon_link_id}", response_model=CharacterWeaponLink)
def update_character_weapon_link(character_weapon_link_id: int, new_weapon_id: int, session: Session = Depends(get_session)):
    link = session.get(CharacterWeaponLink, character_weapon_link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Character-Weapon Link not found")
    
    link.weapon_id = new_weapon_id
    session.commit()
    session.refresh(link)
    return link

# Delete a character’s weapon link
@router.delete("/character_weapons/{character_weapon_link_id}")
def delete_character_weapon_link(character_weapon_link_id: int, session: Session = Depends(get_session)):
    link = session.get(CharacterWeaponLink, character_weapon_link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Character-Weapon Link not found")
    
    session.delete(link)
    session.commit()
    return {"message": "Character-Weapon link deleted successfully"}

# Retrieve all weapons
@router.get("/weapons/", response_model=List[Weapon])
def read_all_weapons(session: Session = Depends(get_session)):
    weapons = session.exec(select(Weapon)).all()
    return weapons

# Retrieve all character weapons
@router.get("/character_weapons/", response_model=List[CharacterWeaponLink])
def read_all_character_weapons(session: Session = Depends(get_session)):
    character_weapons = session.exec(select(CharacterWeaponLink)).all()
    return character_weapons