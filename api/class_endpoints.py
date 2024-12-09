from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import CharacterClass, Character, ClassAbility
from typing import List, Annotated

router = APIRouter()

@router.post("/", response_model=CharacterClass)
def create_character_class(character_class: CharacterClass, session: Session = Depends(get_session)):
    session.add(character_class)
    session.commit()
    session.refresh(character_class)
    return character_class

@router.get("/{character_class_id}", response_model=CharacterClass)
def read_character_class(character_class_id: int, session: Session = Depends(get_session)):
    character_class = session.get(CharacterClass, character_class_id)
    if not character_class:
        raise HTTPException(status_code=404, detail="Character Class not found")
    return character_class

@router.put("/{character_class_id}", response_model=CharacterClass)
def update_character_class(character_class_id: int, character_class_update: CharacterClass, session: Session = Depends(get_session)):
    character_class = session.get(CharacterClass, character_class_id)
    if not character_class:
        raise HTTPException(status_code=404, detail="Character Class not found")
    
    for key, value in character_class_update.dict(exclude_unset=True).items():
        setattr(character_class, key, value)
    
    session.commit()
    session.refresh(character_class)
    return character_class

@router.delete("/{character_class_id}")
def delete_character_class(character_class_id: int, session: Session = Depends(get_session)):
    character_class = session.get(CharacterClass, character_class_id)
    if not character_class:
        raise HTTPException(status_code=404, detail="Character Class not found")
    session.delete(character_class)
    session.commit()
    return {"message": "Character Class deleted successfully"}