from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Feat, Character, CharacterFeatLink
from typing import List

router = APIRouter()

@router.post("/feats/", response_model=Feat)
def create_feat(feat: Feat, session: Session = Depends(get_session)):
    session.add(feat)
    session.commit()
    session.refresh(feat)
    return feat

@router.get("/feats/{feat_id}", response_model=Feat)
def read_feat(feat_id: int, session: Session = Depends(get_session)):
    feat = session.get(Feat, feat_id)
    if not feat:
        raise HTTPException(status_code=404, detail="Feat not found")
    return feat

@router.put("/feats/{feat_id}", response_model=Feat)
def update_feat(feat_id: int, feat_update: Feat, session: Session = Depends(get_session)):
    feat = session.get(Feat, feat_id)
    if not feat:
        raise HTTPException(status_code=404, detail="Feat not found")
    
    for key, value in feat_update.dict(exclude_unset=True).items():
        setattr(feat, key, value)
    
    session.commit()
    session.refresh(feat)
    return feat

@router.delete("/feats/{feat_id}")
def delete_feat(feat_id: int, session: Session = Depends(get_session)):
    feat = session.get(Feat, feat_id)
    if not feat:
        raise HTTPException(status_code=404, detail="Feat not found")
    session.delete(feat)
    session.commit()
    return {"message": "Feat deleted successfully"}

# Create a link between a character and a feat
@router.post("/character_feats/", response_model=CharacterFeatLink)
def create_character_feat_link(character_id: int, feat_id: int, session: Session = Depends(get_session)):
    character = session.get(Character, character_id)
    feat = session.get(Feat, feat_id)
    if not character or not feat:
        raise HTTPException(status_code=404, detail="Character or Feat not found")

    character_feat_link = CharacterFeatLink(character_id=character_id, feat_id=feat_id)
    session.add(character_feat_link)
    session.commit()
    session.refresh(character_feat_link)
    return character_feat_link

# Get all feats for a specific character
@router.get("/character_feats/{character_id}", response_model=List[Feat])
def get_feats_for_character(character_id: int, session: Session = Depends(get_session)):
    feats = session.exec(
        select(Feat).join(CharacterFeatLink).where(CharacterFeatLink.character_id == character_id)
    ).all()
    return feats

# Update a character’s feat link
@router.put("/character_feats/{character_feat_link_id}", response_model=CharacterFeatLink)
def update_character_feat_link(character_feat_link_id: int, new_feat_id: int, session: Session = Depends(get_session)):
    link = session.get(CharacterFeatLink, character_feat_link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Character-Feat Link not found")
    
    link.feat_id = new_feat_id
    session.commit()
    session.refresh(link)
    return link

# Delete a character’s feat link
@router.delete("/character_feats/{character_feat_link_id}")
def delete_character_feat_link(character_feat_link_id: int, session: Session = Depends(get_session)):
    link = session.get(CharacterFeatLink, character_feat_link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Character-Feat Link not found")
    
    session.delete(link)
    session.commit()
    return {"message": "Character-Feat link deleted successfully"}