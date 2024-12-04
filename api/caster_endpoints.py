from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import CasterType
from typing import List

router = APIRouter()

@router.post("/caster_types/", response_model=CasterType)
def create_caster_type(caster_type: CasterType, session: Session = Depends(get_session)):
    session.add(caster_type)
    session.commit()
    session.refresh(caster_type)
    return caster_type

@router.get("/caster_types/{caster_type_id}", response_model=CasterType)
def read_caster_type(caster_type_id: int, session: Session = Depends(get_session)):
    caster_type = session.get(CasterType, caster_type_id)
    if not caster_type:
        raise HTTPException(status_code=404, detail="Caster Type not found")
    return caster_type

@router.put("/caster_types/{caster_type_id}", response_model=CasterType)
def update_caster_type(caster_type_id: int, caster_type_update: CasterType, session: Session = Depends(get_session)):
    caster_type = session.get(CasterType, caster_type_id)
    if not caster_type:
        raise HTTPException(status_code=404, detail="Caster Type not found")
    
    for key, value in caster_type_update.dict(exclude_unset=True).items():
        setattr(caster_type, key, value)
    
    session.commit()
    session.refresh(caster_type)
    return caster_type

@router.delete("/caster_types/{caster_type_id}")
def delete_caster_type(caster_type_id: int, session: Session = Depends(get_session)):
    caster_type = session.get(CasterType, caster_type_id)
    if not caster_type:
        raise HTTPException(status_code=404, detail="Caster Type not found")
    session.delete(caster_type)
    session.commit()
    return {"message": "Caster Type deleted successfully"}

# Retrieve all caster types
@router.get("/caster_types/", response_model=List[CasterType])
def read_all_caster_types(session: Session = Depends(get_session)):
    caster_types = session.exec(select(CasterType)).all()
    return caster_types