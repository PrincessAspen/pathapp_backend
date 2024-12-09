from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import BABProgression
from typing import List

router = APIRouter()

@router.post("/", response_model=BABProgression)
def create_bab_progression(bab_progression: BABProgression, session: Session = Depends(get_session)):
    session.add(bab_progression)
    session.commit()
    session.refresh(bab_progression)
    return bab_progression

@router.get("/{bab_progression_id}", response_model=BABProgression)
def read_bab_progression(bab_progression_id: int, session: Session = Depends(get_session)):
    bab_progression = session.get(BABProgression, bab_progression_id)
    if not bab_progression:
        raise HTTPException(status_code=404, detail="BAB Progression not found")
    return bab_progression

@router.put("/{bab_progression_id}", response_model=BABProgression)
def update_bab_progression(bab_progression_id: int, bab_progression_update: BABProgression, session: Session = Depends(get_session)):
    bab_progression = session.get(BABProgression, bab_progression_id)
    if not bab_progression:
        raise HTTPException(status_code=404, detail="BAB Progression not found")
    
    for key, value in bab_progression_update.dict(exclude_unset=True).items():
        setattr(bab_progression, key, value)
    
    session.commit()
    session.refresh(bab_progression)
    return bab_progression

@router.delete("/{bab_progression_id}")
def delete_bab_progression(bab_progression_id: int, session: Session = Depends(get_session)):
    bab_progression = session.get(BABProgression, bab_progression_id)
    if not bab_progression:
        raise HTTPException(status_code=404, detail="BAB Progression not found")
    session.delete(bab_progression)
    session.commit()
    return {"message": "BAB Progression deleted successfully"}

# Retrieve all BAB progressions
@router.get("/", response_model=List[BABProgression])
def read_all_bab_progressions(session: Session = Depends(get_session)):
    bab_progressions = session.exec(select(BABProgression)).all()
    return bab_progressions