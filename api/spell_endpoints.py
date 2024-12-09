from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Spell, Character, CharacterSpellLink
from typing import List

router = APIRouter()

# Retrieve all spells
@router.get("/", response_model=List[Spell])
def read_all_spells(session: Session = Depends(get_session)):
    spells = session.exec(select(Spell)).all()
    return spells

@router.post("/", response_model=Spell)
def create_spell(spell: Spell, session: Session = Depends(get_session)):
    session.add(spell)
    session.commit()
    session.refresh(spell)
    return spell

@router.get("/{spell_id}", response_model=Spell)
def read_spell(spell_id: int, session: Session = Depends(get_session)):
    spell = session.get(Spell, spell_id)
    if not spell:
        raise HTTPException(status_code=404, detail="Spell not found")
    return spell

@router.put("/{spell_id}", response_model=Spell)
def update_spell(spell_id: int, spell_update: Spell, session: Session = Depends(get_session)):
    spell = session.get(Spell, spell_id)
    if not spell:
        raise HTTPException(status_code=404, detail="Spell not found")
    
    for key, value in spell_update.dict(exclude_unset=True).items():
        setattr(spell, key, value)
    
    session.commit()
    session.refresh(spell)
    return spell

@router.delete("/{spell_id}")
def delete_spell(spell_id: int, session: Session = Depends(get_session)):
    spell = session.get(Spell, spell_id)
    if not spell:
        raise HTTPException(status_code=404, detail="Spell not found")
    session.delete(spell)
    session.commit()
    return {"message": "Spell deleted successfully"}

