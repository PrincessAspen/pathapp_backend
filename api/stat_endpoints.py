from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Stat, CharacterStatLink
from typing import List

router = APIRouter()

@router.post("/stats/", response_model=Stat)
def create_stat(stat: Stat, session: Session = Depends(get_session)):
    session.add(stat)
    session.commit()
    session.refresh(stat)
    return stat

@router.get("/stats/{stat_id}", response_model=Stat)
def read_stat(stat_id: int, session: Session = Depends(get_session)):
    stat = session.get(Stat, stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="Stat not found")
    return stat

@router.put("/stats/{stat_id}", response_model=Stat)
def update_stat(stat_id: int, stat_update: Stat, session: Session = Depends(get_session)):
    stat = session.get(Stat, stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="Stat not found")
    
    for key, value in stat_update.dict(exclude_unset=True).items():
        setattr(stat, key, value)
    
    session.commit()
    session.refresh(stat)
    return stat

@router.delete("/stats/{stat_id}")
def delete_stat(stat_id: int, session: Session = Depends(get_session)):
    stat = session.get(Stat, stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="Stat not found")
    session.delete(stat)
    session.commit()
    return {"message": "Stat deleted successfully"}

@router.post("/character_stats/", response_model=CharacterStatLink)
def create_character_stat_link(character_stat_link: CharacterStatLink, session: Session = Depends(get_session)):
    session.add(character_stat_link)
    session.commit()
    session.refresh(character_stat_link)
    return character_stat_link

@router.get("/character_stats/{character_id}", response_model=List[CharacterStatLink])
def read_character_stat_links(character_id: int, session: Session = Depends(get_session)):
    stat_links = session.exec(select(CharacterStatLink).where(CharacterStatLink.character_id == character_id)).all()
    return stat_links

@router.put("/character_stats/{character_id}/{stat_id}", response_model=CharacterStatLink)
def update_character_stat_link(character_id: int, stat_id: int, stat_link_update: CharacterStatLink, session: Session = Depends(get_session)):
    stat_link = session.get(CharacterStatLink, (character_id, stat_id))
    if not stat_link:
        raise HTTPException(status_code=404, detail="Stat link not found")
    for key, value in stat_link_update.dict(exclude_unset=True).items():
        setattr(stat_link, key, value)
    session.commit()
    session.refresh(stat_link)
    return stat_link

@router.delete("/character_stats/{character_id}/{stat_id}")
def delete_character_stat_link(character_id: int, stat_id: int, session: Session = Depends(get_session)):
    stat_link = session.get(CharacterStatLink, (character_id, stat_id))
    if not stat_link:
        raise HTTPException(status_code=404, detail="Stat link not found")
    session.delete(stat_link)
    session.commit()
    return {"message": "Stat link deleted successfully"}

# Retrieve all stats
@router.get("/stats/", response_model=List[Stat])
def read_all_stats(session: Session = Depends(get_session)):
    stats = session.exec(select(Stat)).all()
    return stats

# Retrieve all character stats links
@router.get("/character_stats/", response_model=List[CharacterStatLink])
def read_all_character_stats(session: Session = Depends(get_session)):
    character_stats = session.exec(select(CharacterStatLink)).all()
    return character_stats