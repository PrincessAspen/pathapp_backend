from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Alignment
from typing import List

router = APIRouter()

@router.post("/alignments/", response_model=Alignment)
def create_alignment(alignment: Alignment, session: Session = Depends(get_session)):
    session.add(alignment)
    session.commit()
    session.refresh(alignment)
    return alignment

@router.get("/alignments/", response_model=List[Alignment])
def read_alignments(session: Session = Depends(get_session)):
    alignments = session.exec(select(Alignment)).all()
    if not alignments:
        raise HTTPException(status_code=404, detail="No alignments found")
    return alignments

@router.get("/alignments/{alignment_id}", response_model=Alignment)
def read_alignment(alignment_id: int, session: Session = Depends(get_session)):
    alignment = session.get(Alignment, alignment_id)
    if not alignment:
        raise HTTPException(status_code=404, detail="Alignment not found")
    return alignment

@router.put("/alignments/{alignment_id}", response_model=Alignment)
def update_alignment(alignment_id: int, alignment_update: Alignment, session: Session = Depends(get_session)):
    alignment = session.get(Alignment, alignment_id)
    if not alignment:
        raise HTTPException(status_code=404, detail="Alignment not found")
    
    for key, value in alignment_update.dict(exclude_unset=True).items():
        setattr(alignment, key, value)
    
    session.commit()
    session.refresh(alignment)
    return alignment

@router.delete("/alignments/{alignment_id}")
def delete_alignment(alignment_id: int, session: Session = Depends(get_session)):
    alignment = session.get(Alignment, alignment_id)
    if not alignment:
        raise HTTPException(status_code=404, detail="Alignment not found")
    session.delete(alignment)
    session.commit()
    return {"message": "Alignment deleted successfully"}

# Retrieve all alignments
@router.get("/alignments/", response_model=List[Alignment])
def read_all_alignments(session: Session = Depends(get_session)):
    alignments = session.exec(select(Alignment)).all()
    return alignments