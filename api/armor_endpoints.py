from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Armor, Character, CharacterArmorLink
from typing import List

router = APIRouter()

@router.post("/", response_model=Armor)
def create_armor(armor: Armor, session: Session = Depends(get_session)):
    session.add(armor)
    session.commit()
    session.refresh(armor)
    return armor

@router.get("/{armor_id}", response_model=Armor)
def read_armor(armor_id: int, session: Session = Depends(get_session)):
    armor = session.get(Armor, armor_id)
    if not armor:
        raise HTTPException(status_code=404, detail="Armor not found")
    return armor

@router.put("/{armor_id}", response_model=Armor)
def update_armor(armor_id: int, armor_update: Armor, session: Session = Depends(get_session)):
    armor = session.get(Armor, armor_id)
    if not armor:
        raise HTTPException(status_code=404, detail="Armor not found")
    
    for key, value in armor_update.dict(exclude_unset=True).items():
        setattr(armor, key, value)
    
    session.commit()
    session.refresh(armor)
    return armor

@router.delete("/{armor_id}")
def delete_armor(armor_id: int, session: Session = Depends(get_session)):
    armor = session.get(Armor, armor_id)
    if not armor:
        raise HTTPException(status_code=404, detail="Armor not found")
    session.delete(armor)
    session.commit()
    return {"message": "Armor deleted successfully"}


# Retrieve all armors
@router.get("/", response_model=List[Armor])
def read_all_armor(session: Session = Depends(get_session)):
    armors = session.exec(select(Armor)).all()
    return armors