from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Race, RacialTrait
from typing import List

router = APIRouter()

@router.get("/races/", response_model=Race)
def read_all_races(session: Session = Depends(get_session)):
    races = session.exec(select(Race)).all()
    return races

@router.post("/races/", response_model=Race)
def create_race(race: Race, session: Session = Depends(get_session)):
    session.add(race)
    session.commit()
    session.refresh(race)
    return race

@router.get("/races/{race_id}", response_model=Race)
def read_race(race_id: int, session: Session = Depends(get_session)):
    race = session.get(Race, race_id)
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    return race

@router.put("/races/{race_id}", response_model=Race)
def update_race(race_id: int, race_update: Race, session: Session = Depends(get_session)):
    race = session.get(Race, race_id)
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    
    for key, value in race_update.dict(exclude_unset=True).items():
        setattr(race, key, value)
    
    session.commit()
    session.refresh(race)
    return race

@router.delete("/races/{race_id}")
def delete_race(race_id: int, session: Session = Depends(get_session)):
    race = session.get(Race, race_id)
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    session.delete(race)
    session.commit()
    return {"message": "Race deleted successfully"}

@router.post("/racial_traits/", response_model=RacialTrait)
def create_racial_trait(racial_trait: RacialTrait, session: Session = Depends(get_session)):
    session.add(racial_trait)
    session.commit()
    session.refresh(racial_trait)
    return racial_trait

@router.get("/racial_traits/{racial_trait_id}", response_model=RacialTrait)
def read_racial_trait(racial_trait_id: int, session: Session = Depends(get_session)):
    racial_trait = session.get(RacialTrait, racial_trait_id)
    if not racial_trait:
        raise HTTPException(status_code=404, detail="Racial Trait not found")
    return racial_trait

@router.put("/racial_traits/{racial_trait_id}", response_model=RacialTrait)
def update_racial_trait(racial_trait_id: int, racial_trait_update: RacialTrait, session: Session = Depends(get_session)):
    racial_trait = session.get(RacialTrait, racial_trait_id)
    if not racial_trait:
        raise HTTPException(status_code=404, detail="Racial Trait not found")
    
    for key, value in racial_trait_update.dict(exclude_unset=True).items():
        setattr(racial_trait, key, value)
    
    session.commit()
    session.refresh(racial_trait)
    return racial_trait

@router.delete("/racial_traits/{racial_trait_id}")
def delete_racial_trait(racial_trait_id: int, session: Session = Depends(get_session)):
    racial_trait = session.get(RacialTrait, racial_trait_id)
    if not racial_trait:
        raise HTTPException(status_code=404, detail="Racial Trait not found")
    session.delete(racial_trait)
    session.commit()
    return {"message": "Racial Trait deleted successfully"}

# Retrieve all racial traits
@router.get("/racial_traits/", response_model=List[RacialTrait])
def read_all_racial_traits(session: Session = Depends(get_session)):
    racial_traits = session.exec(select(RacialTrait)).all()
    return racial_traits