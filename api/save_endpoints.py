from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import SavingThrowProgression
from typing import List

router = APIRouter()

@router.post("/saving_throw_progressions/", response_model=SavingThrowProgression)
def create_saving_throw_progression(saving_throw_progression: SavingThrowProgression, session: Session = Depends(get_session)):
    session.add(saving_throw_progression)
    session.commit()
    session.refresh(saving_throw_progression)
    return saving_throw_progression

@router.get("/saving_throw_progressions/{progression_id}", response_model=SavingThrowProgression)
def read_saving_throw_progression(progression_id: int, session: Session = Depends(get_session)):
    saving_throw_progression = session.get(SavingThrowProgression, progression_id)
    if not saving_throw_progression:
        raise HTTPException(status_code=404, detail="Saving Throw Progression not found")
    return saving_throw_progression

@router.put("/saving_throw_progressions/{progression_id}", response_model=SavingThrowProgression)
def update_saving_throw_progression(progression_id: int, progression_update: SavingThrowProgression, session: Session = Depends(get_session)):
    saving_throw_progression = session.get(SavingThrowProgression, progression_id)
    if not saving_throw_progression:
        raise HTTPException(status_code=404, detail="Saving Throw Progression not found")
    
    for key, value in progression_update.dict(exclude_unset=True).items():
        setattr(saving_throw_progression, key, value)
    
    session.commit()
    session.refresh(saving_throw_progression)
    return saving_throw_progression

@router.delete("/saving_throw_progressions/{progression_id}")
def delete_saving_throw_progression(progression_id: int, session: Session = Depends(get_session)):
    saving_throw_progression = session.get(SavingThrowProgression, progression_id)
    if not saving_throw_progression:
        raise HTTPException(status_code=404, detail="Saving Throw Progression not found")
    session.delete(saving_throw_progression)
    session.commit()
    return {"message": "Saving Throw Progression deleted successfully"}

# Retrieve all saving throw progressions
@router.get("/saving_throw_progressions/", response_model=List[SavingThrowProgression])
def read_all_saving_throw_progressions(session: Session = Depends(get_session)):
    saving_throw_progressions = session.exec(select(SavingThrowProgression)).all()
    return saving_throw_progressions