from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Stat, CharacterStatLink
from typing import List

router = APIRouter()

# Retrieve all stats
@router.get("/", response_model=List[Stat])
def read_all_stats(session: Session = Depends(get_session)):
    stats = session.exec(select(Stat)).all()
    return stats

@router.post("/", response_model=Stat)
def create_stat(stat: Stat, session: Session = Depends(get_session)):
    session.add(stat)
    session.commit()
    session.refresh(stat)
    return stat

@router.get("/{stat_id}", response_model=Stat)
def read_stat(stat_id: int, session: Session = Depends(get_session)):
    stat = session.get(Stat, stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="Stat not found")
    return stat

@router.put("/{stat_id}", response_model=Stat)
def update_stat(stat_id: int, stat_update: Stat, session: Session = Depends(get_session)):
    stat = session.get(Stat, stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="Stat not found")
    
    for key, value in stat_update.dict(exclude_unset=True).items():
        setattr(stat, key, value)
    
    session.commit()
    session.refresh(stat)
    return stat

@router.delete("/{stat_id}")
def delete_stat(stat_id: int, session: Session = Depends(get_session)):
    stat = session.get(Stat, stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="Stat not found")
    session.delete(stat)
    session.commit()
    return {"message": "Stat deleted successfully"}

