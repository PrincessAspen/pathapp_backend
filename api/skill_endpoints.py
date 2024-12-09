from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Skill, CharacterSkillLink
from typing import List

router = APIRouter()


# Retrieve all skills
@router.get("/", response_model=List[Skill])
def read_all_skills(session: Session = Depends(get_session)):
    skills = session.exec(select(Skill)).all()
    return skills

@router.post("/", response_model=Skill)
def create_skill(skill: Skill, session: Session = Depends(get_session)):
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill

@router.get("/{skill_id}", response_model=Skill)
def read_skill(skill_id: int, session: Session = Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@router.put("/{skill_id}", response_model=Skill)
def update_skill(skill_id: int, skill_update: Skill, session: Session = Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    for key, value in skill_update.dict(exclude_unset=True).items():
        setattr(skill, key, value)
    
    session.commit()
    session.refresh(skill)
    return skill

@router.delete("/{skill_id}")
def delete_skill(skill_id: int, session: Session = Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    session.delete(skill)
    session.commit()
    return {"message": "Skill deleted successfully"}

