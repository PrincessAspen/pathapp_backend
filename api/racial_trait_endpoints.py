from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Race, RacialTrait
from typing import List

router = APIRouter()

@router.post("/", response_model=RacialTrait)
def create_racial_trait(racial_trait: RacialTrait, session: Session = Depends(get_session)):
    session.add(racial_trait)
    session.commit()
    session.refresh(racial_trait)
    return racial_trait

@router.get("/{racial_trait_id}", response_model=RacialTrait)
def read_racial_trait(racial_trait_id: int, session: Session = Depends(get_session)):
    racial_trait = session.get(RacialTrait, racial_trait_id)
    if not racial_trait:
        raise HTTPException(status_code=404, detail="Racial Trait not found")
    return racial_trait

@router.put("/{racial_trait_id}", response_model=RacialTrait)
def update_racial_trait(racial_trait_id: int, racial_trait_update: RacialTrait, session: Session = Depends(get_session)):
    racial_trait = session.get(RacialTrait, racial_trait_id)
    if not racial_trait:
        raise HTTPException(status_code=404, detail="Racial Trait not found")
    
    for key, value in racial_trait_update.dict(exclude_unset=True).items():
        setattr(racial_trait, key, value)
    
    session.commit()
    session.refresh(racial_trait)
    return racial_trait

@router.delete("/{racial_trait_id}")
def delete_racial_trait(racial_trait_id: int, session: Session = Depends(get_session)):
    racial_trait = session.get(RacialTrait, racial_trait_id)
    if not racial_trait:
        raise HTTPException(status_code=404, detail="Racial Trait not found")
    session.delete(racial_trait)
    session.commit()
    return {"message": "Racial Trait deleted successfully"}

# Retrieve all racial traits
@router.get("/", response_model=List[RacialTrait])
def read_all_racial_traits(session: Session = Depends(get_session)):
    racial_traits = session.exec(select(RacialTrait)).all()
    return racial_traits