from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Spell, Character, CharacterSpellLink
from typing import List

router = APIRouter()

@router.post("/spells/", response_model=Spell)
def create_spell(spell: Spell, session: Session = Depends(get_session)):
    session.add(spell)
    session.commit()
    session.refresh(spell)
    return spell

@router.get("/spells/{spell_id}", response_model=Spell)
def read_spell(spell_id: int, session: Session = Depends(get_session)):
    spell = session.get(Spell, spell_id)
    if not spell:
        raise HTTPException(status_code=404, detail="Spell not found")
    return spell

@router.put("/spells/{spell_id}", response_model=Spell)
def update_spell(spell_id: int, spell_update: Spell, session: Session = Depends(get_session)):
    spell = session.get(Spell, spell_id)
    if not spell:
        raise HTTPException(status_code=404, detail="Spell not found")
    
    for key, value in spell_update.dict(exclude_unset=True).items():
        setattr(spell, key, value)
    
    session.commit()
    session.refresh(spell)
    return spell

@router.delete("/spells/{spell_id}")
def delete_spell(spell_id: int, session: Session = Depends(get_session)):
    spell = session.get(Spell, spell_id)
    if not spell:
        raise HTTPException(status_code=404, detail="Spell not found")
    session.delete(spell)
    session.commit()
    return {"message": "Spell deleted successfully"}

# Create a link between a character and a spell
@router.post("/character_spells/", response_model=CharacterSpellLink)
def create_character_spell_link(character_id: int, spell_id: int, session: Session = Depends(get_session)):
    # Verify both character and spell exist
    character = session.get(Character, character_id)
    spell = session.get(Spell, spell_id)
    if not character or not spell:
        raise HTTPException(status_code=404, detail="Character or Spell not found")
    
    # Create the link
    character_spell_link = CharacterSpellLink(character_id=character_id, spell_id=spell_id)
    session.add(character_spell_link)
    session.commit()
    session.refresh(character_spell_link)
    return character_spell_link

# Get all spells for a specific character
@router.get("/character_spells/{character_id}", response_model=List[Spell])
def get_spells_for_character(character_id: int, session: Session = Depends(get_session)):
    character = session.get(Character, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    # Query to retrieve all spells linked to this character
    spells = session.exec(
        select(Spell).join(CharacterSpellLink).where(CharacterSpellLink.character_id == character_id)
    ).all()
    return spells

# Update a character's spell link (changing a spell for a character)
@router.put("/character_spells/{character_spell_link_id}", response_model=CharacterSpellLink)
def update_character_spell_link(character_spell_link_id: int, new_spell_id: int, session: Session = Depends(get_session)):
    link = session.get(CharacterSpellLink, character_spell_link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Character-Spell Link not found")
    
    new_spell = session.get(Spell, new_spell_id)
    if not new_spell:
        raise HTTPException(status_code=404, detail="New Spell not found")

    # Update the link
    link.spell_id = new_spell_id
    session.commit()
    session.refresh(link)
    return link

# Delete a character's spell link
@router.delete("/character_spells/{character_spell_link_id}")
def delete_character_spell_link(character_spell_link_id: int, session: Session = Depends(get_session)):
    link = session.get(CharacterSpellLink, character_spell_link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Character-Spell Link not found")
    
    session.delete(link)
    session.commit()
    return {"message": "Character-Spell link deleted successfully"}

# Retrieve all spells
@router.get("/spells/", response_model=List[Spell])
def read_all_spells(session: Session = Depends(get_session)):
    spells = session.exec(select(Spell)).all()
    return spells

# Retrieve all character spells
@router.get("/character_spells/", response_model=List[CharacterSpellLink])
def read_all_character_spells(session: Session = Depends(get_session)):
    character_spells = session.exec(select(CharacterSpellLink)).all()
    return character_spells