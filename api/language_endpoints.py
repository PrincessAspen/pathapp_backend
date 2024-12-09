from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Language
from typing import List

router = APIRouter()

@router.post("/", response_model=Language)
def create_language(language: Language, session: Session = Depends(get_session)):
    session.add(language)
    session.commit()
    session.refresh(language)
    return language

@router.get("/{language_id}", response_model=Language)
def read_language(language_id: int, session: Session = Depends(get_session)):
    language = session.get(Language, language_id)
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    return language

@router.put("/{language_id}", response_model=Language)
def update_language(language_id: int, language_update: Language, session: Session = Depends(get_session)):
    language = session.get(Language, language_id)
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    
    for key, value in language_update.dict(exclude_unset=True).items():
        setattr(language, key, value)
    
    session.commit()
    session.refresh(language)
    return language

@router.delete("/{language_id}")
def delete_language(language_id: int, session: Session = Depends(get_session)):
    language = session.get(Language, language_id)
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    session.delete(language)
    session.commit()
    return {"message": "Language deleted successfully"}

# Retrieve all languages
@router.get("/", response_model=List[Language])
def read_all_languages(session: Session = Depends(get_session)):
    languages = session.exec(select(Language)).all()
    return languages