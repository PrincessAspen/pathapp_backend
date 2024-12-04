from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Equipment, CharacterInventoryLink, Character
from typing import List

router = APIRouter()

@router.post("/equipment/", response_model=Equipment)
def create_equipment(equipment: Equipment, session: Session = Depends(get_session)):
    session.add(equipment)
    session.commit()
    session.refresh(equipment)
    return equipment

@router.get("/equipment/{equipment_id}", response_model=Equipment)
def read_equipment(equipment_id: int, session: Session = Depends(get_session)):
    equipment = session.get(Equipment, equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@router.put("/equipment/{equipment_id}", response_model=Equipment)
def update_equipment(equipment_id: int, equipment_update: Equipment, session: Session = Depends(get_session)):
    equipment = session.get(Equipment, equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    for key, value in equipment_update.dict(exclude_unset=True).items():
        setattr(equipment, key, value)
    
    session.commit()
    session.refresh(equipment)
    return equipment

@router.delete("/equipment/{equipment_id}")
def delete_equipment(equipment_id: int, session: Session = Depends(get_session)):
    equipment = session.get(Equipment, equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    session.delete(equipment)
    session.commit()
    return {"message": "Equipment deleted successfully"}

@router.put("/character_inventory/{character_id}/{equipment_id}", response_model=CharacterInventoryLink)
def update_character_inventory_link(character_id: int, equipment_id: int, inventory_link_update: CharacterInventoryLink, session: Session = Depends(get_session)):
    inventory_link = session.get(CharacterInventoryLink, (character_id, equipment_id))
    if not inventory_link:
        raise HTTPException(status_code=404, detail="Inventory link not found")
    for key, value in inventory_link_update.dict(exclude_unset=True).items():
        setattr(inventory_link, key, value)
    session.commit()
    session.refresh(inventory_link)
    return inventory_link

@router.delete("/character_inventory/{character_id}/{equipment_id}")
def delete_character_inventory_link(character_id: int, equipment_id: int, session: Session = Depends(get_session)):
    inventory_link = session.get(CharacterInventoryLink, (character_id, equipment_id))
    if not inventory_link:
        raise HTTPException(status_code=404, detail="Inventory link not found")
    session.delete(inventory_link)
    session.commit()
    return {"message": "Inventory link deleted successfully"}

@router.post("/character_inventory/", response_model=CharacterInventoryLink)
def create_character_inventory_link(character_inventory_link: CharacterInventoryLink, session: Session = Depends(get_session)):
    session.add(character_inventory_link)
    session.commit()
    session.refresh(character_inventory_link)
    return character_inventory_link

@router.get("/character_inventory/{character_id}", response_model=List[CharacterInventoryLink])
def read_character_inventory_links(character_id: int, session: Session = Depends(get_session)):
    inventory_links = session.exec(select(CharacterInventoryLink).where(CharacterInventoryLink.character_id == character_id)).all()
    return inventory_links

# Retrieve all character inventory links
@router.get("/character_inventory/", response_model=List[CharacterInventoryLink])
def read_all_character_inventory(session: Session = Depends(get_session)):
    character_inventory = session.exec(select(CharacterInventoryLink)).all()
    return character_inventory

# Retrieve all equipment
@router.get("/equipment/", response_model=List[Equipment])
def read_all_equipment(session: Session = Depends(get_session)):
    equipment = session.exec(select(Equipment)).all()
    return equipment