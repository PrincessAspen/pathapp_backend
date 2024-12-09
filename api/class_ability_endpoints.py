from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import CharacterClass, Character, ClassAbility
from typing import List, Annotated

router = APIRouter()

@router.post("/", response_model=ClassAbility)
def create_class_ability(class_ability: ClassAbility, session: Session = Depends(get_session)):
    session.add(class_ability)
    session.commit()
    session.refresh(class_ability)
    return class_ability

@router.get("/{ability_id}", response_model=ClassAbility)
def read_class_ability(ability_id: int, session: Session = Depends(get_session)):
    class_ability = session.get(ClassAbility, ability_id)
    if not class_ability:
        raise HTTPException(status_code=404, detail="Class Ability not found")
    return class_ability

@router.put("/{ability_id}", response_model=ClassAbility)
def update_class_ability(ability_id: int, ability_update: ClassAbility, session: Session = Depends(get_session)):
    class_ability = session.get(ClassAbility, ability_id)
    if not class_ability:
        raise HTTPException(status_code=404, detail="Class Ability not found")
    
    for key, value in ability_update.dict(exclude_unset=True).items():
        setattr(class_ability, key, value)
    
    session.commit()
    session.refresh(class_ability)
    return class_ability

@router.delete("/{ability_id}")
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
@router.get("/", response_model=List[ClassAbility])
def read_all_class_abilities(session: Session = Depends(get_session)):
    class_abilities = session.exec(select(ClassAbility)).all()
    return class_abilities