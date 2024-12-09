from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Race, RacialTrait
from typing import List

router = APIRouter()

@router.get("/", response_model=Race)
def read_all_races(session: Session = Depends(get_session)):
    races = session.exec(select(Race)).all()
    return races

@router.post("/", response_model=Race)
def create_race(race: Race, session: Session = Depends(get_session)):
    session.add(race)
    session.commit()
    session.refresh(race)
    return race

@router.get("/{race_id}", response_model=Race)
def read_race(race_id: int, session: Session = Depends(get_session)):
    race = session.get(Race, race_id)
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    return race

@router.put("/{race_id}", response_model=Race)
def update_race(race_id: int, race_update: Race, session: Session = Depends(get_session)):
    race = session.get(Race, race_id)
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    
    for key, value in race_update.dict(exclude_unset=True).items():
        setattr(race, key, value)
    
    session.commit()
    session.refresh(race)
    return race

@router.delete("/{race_id}")
def delete_race(race_id: int, session: Session = Depends(get_session)):
    race = session.get(Race, race_id)
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    session.delete(race)
    session.commit()
    return {"message": "Race deleted successfully"}