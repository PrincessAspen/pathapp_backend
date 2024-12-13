from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from db import get_session
from models import Class, Race, Stat, Skill, Feat, Alignment
from typing import Dict, List

router = APIRouter()

@router.get("/", response_model=Dict[str, List])
def get_character_creation_data(session: Session = Depends(get_session)):
    """
    Returns all the data required for character creation in a single response.
    """
    classes = session.exec(select(Class)).all()
    races = session.exec(select(Race)).all()
    stats = session.exec(select(Stat)).all()
    skills = session.exec(select(Skill)).all()
    feats = session.exec(select(Feat)).all()
    alignments = session.exec(select(Alignment)).all()

    return {
        "classes": classes,
        "races": races,
        "stats": stats,
        "skills": skills,
        "feats": feats,
        "alignments": alignments,
    }
