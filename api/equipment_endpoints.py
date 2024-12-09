from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Equipment, CharacterInventoryLink, Character
from typing import List

router = APIRouter()

@router.post("/", response_model=Equipment)
def create_equipment(equipment: Equipment, session: Session = Depends(get_session)):
    session.add(equipment)
    session.commit()
    session.refresh(equipment)
    return equipment

@router.get("/{equipment_id}", response_model=Equipment)
def read_equipment(equipment_id: int, session: Session = Depends(get_session)):
    equipment = session.get(Equipment, equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@router.put("/{equipment_id}", response_model=Equipment)
def update_equipment(equipment_id: int, equipment_update: Equipment, session: Session = Depends(get_session)):
    equipment = session.get(Equipment, equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    for key, value in equipment_update.dict(exclude_unset=True).items():
        setattr(equipment, key, value)
    
    session.commit()
    session.refresh(equipment)
    return equipment

@router.delete("/{equipment_id}")
def delete_equipment(equipment_id: int, session: Session = Depends(get_session)):
    equipment = session.get(Equipment, equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    session.delete(equipment)
    session.commit()
    return {"message": "Equipment deleted successfully"}



# Retrieve all equipment
@router.get("/", response_model=List[Equipment])
def read_all_equipment(session: Session = Depends(get_session)):
    equipment = session.exec(select(Equipment)).all()
    return equipment