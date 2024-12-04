from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Armor, Character, CharacterArmorLink
from typing import List

router = APIRouter()

@router.post("/armor/", response_model=Armor)
def create_armor(armor: Armor, session: Session = Depends(get_session)):
    session.add(armor)
    session.commit()
    session.refresh(armor)
    return armor

@router.get("/armor/{armor_id}", response_model=Armor)
def read_armor(armor_id: int, session: Session = Depends(get_session)):
    armor = session.get(Armor, armor_id)
    if not armor:
        raise HTTPException(status_code=404, detail="Armor not found")
    return armor

@router.put("/armor/{armor_id}", response_model=Armor)
def update_armor(armor_id: int, armor_update: Armor, session: Session = Depends(get_session)):
    armor = session.get(Armor, armor_id)
    if not armor:
        raise HTTPException(status_code=404, detail="Armor not found")
    
    for key, value in armor_update.dict(exclude_unset=True).items():
        setattr(armor, key, value)
    
    session.commit()
    session.refresh(armor)
    return armor

@router.delete("/armor/{armor_id}")
def delete_armor(armor_id: int, session: Session = Depends(get_session)):
    armor = session.get(Armor, armor_id)
    if not armor:
        raise HTTPException(status_code=404, detail="Armor not found")
    session.delete(armor)
    session.commit()
    return {"message": "Armor deleted successfully"}

# Create a link between a character and an armor
@router.post("/character_armors/", response_model=CharacterArmorLink)
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
@router.get("/character_armors/{character_id}", response_model=List[Armor])
def get_armor_for_character(character_id: int, session: Session = Depends(get_session)):
    armors = session.exec(
        select(Armor).join(CharacterArmorLink).where(CharacterArmorLink.character_id == character_id)
    ).all()
    return armors

# Update a character’s armor link
@router.put("/character_armors/{character_armor_link_id}", response_model=CharacterArmorLink)
def update_character_armor_link(character_armor_link_id: int, new_armor_id: int, session: Session = Depends(get_session)):
    link = session.get(CharacterArmorLink, character_armor_link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Character-Armor Link not found")
    
    link.armor_id = new_armor_id
    session.commit()
    session.refresh(link)
    return link

# Delete a character’s armor link
@router.delete("/character_armors/{character_armor_link_id}")
def delete_character_armor_link(character_armor_link_id: int, session: Session = Depends(get_session)):
    link = session.get(CharacterArmorLink, character_armor_link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Character-Armor Link not found")
    
    session.delete(link)
    session.commit()
    return {"message": "Character-Armor link deleted successfully"}

# Retrieve all armors
@router.get("/armor/", response_model=List[Armor])
def read_all_armor(session: Session = Depends(get_session)):
    armors = session.exec(select(Armor)).all()
    return armors