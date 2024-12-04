from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import MoneyValue, CharacterMoneyLink
from typing import List

router = APIRouter()

@router.post("/money_values/", response_model=MoneyValue)
def create_money_value(money_value: MoneyValue, session: Session = Depends(get_session)):
    session.add(money_value)
    session.commit()
    session.refresh(money_value)
    return money_value

@router.get("/money_values/{money_value_id}", response_model=MoneyValue)
def read_money_value(money_value_id: int, session: Session = Depends(get_session)):
    money_value = session.get(MoneyValue, money_value_id)
    if not money_value:
        raise HTTPException(status_code=404, detail="Money Value not found")
    return money_value

@router.put("/money_values/{money_value_id}", response_model=MoneyValue)
def update_money_value(money_value_id: int, money_value_update: MoneyValue, session: Session = Depends(get_session)):
    money_value = session.get(MoneyValue, money_value_id)
    if not money_value:
        raise HTTPException(status_code=404, detail="Money Value not found")
    
    for key, value in money_value_update.dict(exclude_unset=True).items():
        setattr(money_value, key, value)
    
    session.commit()
    session.refresh(money_value)
    return money_value

@router.delete("/money_values/{money_value_id}")
def delete_money_value(money_value_id: int, session: Session = Depends(get_session)):
    money_value = session.get(MoneyValue, money_value_id)
    if not money_value:
        raise HTTPException(status_code=404, detail="Money Value not found")
    session.delete(money_value)
    session.commit()
    return {"message": "Money Value deleted successfully"}

@router.post("/character_money/", response_model=CharacterMoneyLink)
def create_character_money_link(character_money_link: CharacterMoneyLink, session: Session = Depends(get_session)):
    session.add(character_money_link)
    session.commit()
    session.refresh(character_money_link)
    return character_money_link

@router.get("/character_money/{character_id}", response_model=List[CharacterMoneyLink])
def read_character_money_links(character_id: int, session: Session = Depends(get_session)):
    money_links = session.exec(select(CharacterMoneyLink).where(CharacterMoneyLink.character_id == character_id)).all()
    return money_links

@router.put("/character_money/{character_id}/{money_id}", response_model=CharacterMoneyLink)
def update_character_money_link(character_id: int, money_id: int, money_link_update: CharacterMoneyLink, session: Session = Depends(get_session)):
    money_link = session.get(CharacterMoneyLink, (character_id, money_id))
    if not money_link:
        raise HTTPException(status_code=404, detail="Money link not found")
    for key, value in money_link_update.dict(exclude_unset=True).items():
        setattr(money_link, key, value)
    session.commit()
    session.refresh(money_link)
    return money_link

@router.delete("/character_money/{character_id}/{money_id}")
def delete_character_money_link(character_id: int, money_id: int, session: Session = Depends(get_session)):
    money_link = session.get(CharacterMoneyLink, (character_id, money_id))
    if not money_link:
        raise HTTPException(status_code=404, detail="Money link not found")
    session.delete(money_link)
    session.commit()
    return {"message": "Money link deleted successfully"}

# Retrieve all character money links
@router.get("/character_money/", response_model=List[CharacterMoneyLink])
def read_all_character_money(session: Session = Depends(get_session)):
    character_money = session.exec(select(CharacterMoneyLink)).all()
    return character_money

# Retrieve all money values
@router.get("/money_values/", response_model=List[MoneyValue])
def read_all_money_values(session: Session = Depends(get_session)):
    money_values = session.exec(select(MoneyValue)).all()
    return money_values