from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import CharacterClass, Character, ClassAbility
from typing import List, Annotated

router = APIRouter()

@router.post("/character_classes/", response_model=CharacterClass)
def create_character_class(character_class: CharacterClass, session: Session = Depends(get_session)):
    session.add(character_class)
    session.commit()
    session.refresh(character_class)
    return character_class

@router.get("/character_classes/{character_class_id}", response_model=CharacterClass)
def read_character_class(character_class_id: int, session: Session = Depends(get_session)):
    character_class = session.get(CharacterClass, character_class_id)
    if not character_class:
        raise HTTPException(status_code=404, detail="Character Class not found")
    return character_class

@router.put("/character_classes/{character_class_id}", response_model=CharacterClass)
def update_character_class(character_class_id: int, character_class_update: CharacterClass, session: Session = Depends(get_session)):
    character_class = session.get(CharacterClass, character_class_id)
    if not character_class:
        raise HTTPException(status_code=404, detail="Character Class not found")
    
    for key, value in character_class_update.dict(exclude_unset=True).items():
        setattr(character_class, key, value)
    
    session.commit()
    session.refresh(character_class)
    return character_class

@router.delete("/character_classes/{character_class_id}")
def delete_character_class(character_class_id: int, session: Session = Depends(get_session)):
    character_class = session.get(CharacterClass, character_class_id)
    if not character_class:
        raise HTTPException(status_code=404, detail="Character Class not found")
    session.delete(character_class)
    session.commit()
    return {"message": "Character Class deleted successfully"}

@router.post("/class_abilities/", response_model=ClassAbility)
def create_class_ability(class_ability: ClassAbility, session: Session = Depends(get_session)):
    session.add(class_ability)
    session.commit()
    session.refresh(class_ability)
    return class_ability

@router.get("/class_abilities/{ability_id}", response_model=ClassAbility)
def read_class_ability(ability_id: int, session: Session = Depends(get_session)):
    class_ability = session.get(ClassAbility, ability_id)
    if not class_ability:
        raise HTTPException(status_code=404, detail="Class Ability not found")
    return class_ability

@router.put("/class_abilities/{ability_id}", response_model=ClassAbility)
def update_class_ability(ability_id: int, ability_update: ClassAbility, session: Session = Depends(get_session)):
    class_ability = session.get(ClassAbility, ability_id)
    if not class_ability:
        raise HTTPException(status_code=404, detail="Class Ability not found")
    
    for key, value in ability_update.dict(exclude_unset=True).items():
        setattr(class_ability, key, value)
    
    session.commit()
    session.refresh(class_ability)
    return class_ability

@router.delete("/class_abilities/{ability_id}")
def delete_class_ability(ability_id: int, session: Session = Depends(get_session)):
    class_ability = session.get(ClassAbility, ability_id)
    if not class_ability:
        raise HTTPException(status_code=404, detail="Class Ability not found")
    session.delete(class_ability)
    session.commit()
    return {"message": "Class Ability deleted successfully"}

# Retrieve all character classes
@router.get("/character_classes/", response_model=List[CharacterClass])
def read_all_character_classes(session: Session = Depends(get_session)):
    character_classes = session.exec(select(CharacterClass)).all()
    return character_classes

# Retrieve all class abilities
@router.get("/class_abilities/", response_model=List[ClassAbility])
def read_all_class_abilities(session: Session = Depends(get_session)):
    class_abilities = session.exec(select(ClassAbility)).all()
    return class_abilities