from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Feat, Character, CharacterFeatLink
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Feat])
def read_all_feats(session: Session = Depends(get_session)):
    feats = session.exec(select(Feat)).all()
    return feats

@router.post("/", response_model=Feat)
def create_feat(feat: Feat, session: Session = Depends(get_session)):
    session.add(feat)
    session.commit()
    session.refresh(feat)
    return feat

@router.get("/{feat_id}", response_model=Feat)
def read_feat(feat_id: int, session: Session = Depends(get_session)):
    feat = session.get(Feat, feat_id)
    if not feat:
        raise HTTPException(status_code=404, detail="Feat not found")
    return feat

@router.put("/{feat_id}", response_model=Feat)
def update_feat(feat_id: int, feat_update: Feat, session: Session = Depends(get_session)):
    feat = session.get(Feat, feat_id)
    if not feat:
        raise HTTPException(status_code=404, detail="Feat not found")
    
    for key, value in feat_update.dict(exclude_unset=True).items():
        setattr(feat, key, value)
    
    session.commit()
    session.refresh(feat)
    return feat

@router.delete("/{feat_id}")
def delete_feat(feat_id: int, session: Session = Depends(get_session)):
    feat = session.get(Feat, feat_id)
    if not feat:
        raise HTTPException(status_code=404, detail="Feat not found")
    session.delete(feat)
    session.commit()
    return {"message": "Feat deleted successfully"}

