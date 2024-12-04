from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Skill, CharacterSkillLink
from typing import List

router = APIRouter()

@router.post("/skills/", response_model=Skill)
def create_skill(skill: Skill, session: Session = Depends(get_session)):
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill

@router.get("/skills/{skill_id}", response_model=Skill)
def read_skill(skill_id: int, session: Session = Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@router.put("/skills/{skill_id}", response_model=Skill)
def update_skill(skill_id: int, skill_update: Skill, session: Session = Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    for key, value in skill_update.dict(exclude_unset=True).items():
        setattr(skill, key, value)
    
    session.commit()
    session.refresh(skill)
    return skill

@router.delete("/skills/{skill_id}")
def delete_skill(skill_id: int, session: Session = Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    session.delete(skill)
    session.commit()
    return {"message": "Skill deleted successfully"}

# CRUD for character skill link

@router.post("/character_skills/", response_model=CharacterSkillLink)
def create_character_skill_link(character_skill_link: CharacterSkillLink, session: Session = Depends(get_session)):
    session.add(character_skill_link)
    session.commit()
    session.refresh(character_skill_link)
    return character_skill_link

@router.get("/character_skills/{character_id}", response_model=List[CharacterSkillLink])
def read_character_skill_links(character_id: int, session: Session = Depends(get_session)):
    skill_links = session.exec(select(CharacterSkillLink).where(CharacterSkillLink.character_id == character_id)).all()
    return skill_links

@router.put("/character_skills/{character_id}/{skill_id}", response_model=CharacterSkillLink)
def update_character_skill_link(character_id: int, skill_id: int, skill_link_update: CharacterSkillLink, session: Session = Depends(get_session)):
    skill_link = session.get(CharacterSkillLink, (character_id, skill_id))
    if not skill_link:
        raise HTTPException(status_code=404, detail="Skill link not found")
    for key, value in skill_link_update.dict(exclude_unset=True).items():
        setattr(skill_link, key, value)
    session.commit()
    session.refresh(skill_link)
    return skill_link

@router.delete("/character_skills/{character_id}/{skill_id}")
def delete_character_skill_link(character_id: int, skill_id: int, session: Session = Depends(get_session)):
    skill_link = session.get(CharacterSkillLink, (character_id, skill_id))
    if not skill_link:
        raise HTTPException(status_code=404, detail="Skill link not found")
    session.delete(skill_link)
    session.commit()
    return {"message": "Skill link deleted successfully"}

# Retrieve all skills
@router.get("/skills/", response_model=List[Skill])
def read_all_skills(session: Session = Depends(get_session)):
    skills = session.exec(select(Skill)).all()
    return skills

# Retrieve all character skills links
@router.get("/character_skills/", response_model=List[CharacterSkillLink])
def read_all_character_skills(session: Session = Depends(get_session)):
    character_skills = session.exec(select(CharacterSkillLink)).all()
    return character_skills