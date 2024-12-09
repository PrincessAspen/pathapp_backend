from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Weapon, Character, CharacterWeaponLink
from typing import List

router = APIRouter()

# Retrieve all weapons
@router.get("/", response_model=List[Weapon])
def read_all_weapons(session: Session = Depends(get_session)):
    weapons = session.exec(select(Weapon)).all()
    return weapons

@router.post("/", response_model=Weapon)
def create_weapon(weapon: Weapon, session: Session = Depends(get_session)):
    session.add(weapon)
    session.commit()
    session.refresh(weapon)
    return weapon

@router.get("/{weapon_id}", response_model=Weapon)
def read_weapon(weapon_id: int, session: Session = Depends(get_session)):
    weapon = session.get(Weapon, weapon_id)
    if not weapon:
        raise HTTPException(status_code=404, detail="Weapon not found")
    return weapon

@router.put("/{weapon_id}", response_model=Weapon)
def update_weapon(weapon_id: int, weapon_update: Weapon, session: Session = Depends(get_session)):
    weapon = session.get(Weapon, weapon_id)
    if not weapon:
        raise HTTPException(status_code=404, detail="Weapon not found")
    
    for key, value in weapon_update.dict(exclude_unset=True).items():
        setattr(weapon, key, value)
    
    session.commit()
    session.refresh(weapon)
    return weapon

@router.delete("/{weapon_id}")
def delete_weapon(weapon_id: int, session: Session = Depends(get_session)):
    weapon = session.get(Weapon, weapon_id)
    if not weapon:
        raise HTTPException(status_code=404, detail="Weapon not found")
    session.delete(weapon)
    session.commit()
    return {"message": "Weapon deleted successfully"}