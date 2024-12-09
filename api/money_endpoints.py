from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import MoneyValue, CharacterMoneyLink
from typing import List

router = APIRouter()

@router.post("/", response_model=MoneyValue)
def create_money_value(money_value: MoneyValue, session: Session = Depends(get_session)):
    session.add(money_value)
    session.commit()
    session.refresh(money_value)
    return money_value

@router.get("/{money_value_id}", response_model=MoneyValue)
def read_money_value(money_value_id: int, session: Session = Depends(get_session)):
    money_value = session.get(MoneyValue, money_value_id)
    if not money_value:
        raise HTTPException(status_code=404, detail="Money Value not found")
    return money_value

@router.put("/{money_value_id}", response_model=MoneyValue)
def update_money_value(money_value_id: int, money_value_update: MoneyValue, session: Session = Depends(get_session)):
    money_value = session.get(MoneyValue, money_value_id)
    if not money_value:
        raise HTTPException(status_code=404, detail="Money Value not found")
    
    for key, value in money_value_update.dict(exclude_unset=True).items():
        setattr(money_value, key, value)
    
    session.commit()
    session.refresh(money_value)
    return money_value

@router.delete("/{money_value_id}")
def delete_money_value(money_value_id: int, session: Session = Depends(get_session)):
    money_value = session.get(MoneyValue, money_value_id)
    if not money_value:
        raise HTTPException(status_code=404, detail="Money Value not found")
    session.delete(money_value)
    session.commit()
    return {"message": "Money Value deleted successfully"}


# Retrieve all money values
@router.get("/", response_model=List[MoneyValue])
def read_all_money_values(session: Session = Depends(get_session)):
    money_values = session.exec(select(MoneyValue)).all()
    return money_values