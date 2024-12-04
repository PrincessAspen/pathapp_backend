import uvicorn
import jwt
from typing import List, Annotated
from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from db import get_session
from models import Race, RacialTrait, Character
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from config import SUPABASE_SECRET_KEY, JWT_ALGORITHM   
from api.race_endpoints import router as race_router
from api.armor_endpoints import router as armor_router
from api.alignment_endpoints import router as alignment_router
from api.class_endpoints import router as class_router
from api.bab_endpoints import router as bab_router
from api.caster_endpoints import router as caster_router
from api.feat_endpoints import router as feat_router
from api.stat_endpoints import router as stat_router
from api.save_endpoints import router as save_router
from api.equipment_endpoints import router as equipment_router
from api.skill_endpoints import router as skill_router
from api.money_endpoints import router as money_router
from api.language_endpoints import router as language_router

app = FastAPI(redirect_slashes=False)

app.include_router(race_router, prefix="/races", tags=["Races"])
app.include_router(race_router, prefix="/racial_traits", tags=["Racial Traits"])
app.include_router(armor_router, prefix="/armor", tags=["Armor"])
app.include_router(alignment_router, prefix="/alignments", tags=["Alignments"])
app.include_router(class_router, prefix="/classes", tags=["Classes"])
app.include_router(class_router, prefix="/class_abilities", tags=["Class Abilities"])
app.include_router(bab_router, prefix="/bab_progressions", tags=["Base Attack Bonus"])
app.include_router(caster_router, prefix="/caster_types", tags=["Caster Types"])
app.include_router(feat_router, prefix="/feats", tags=["Feats"])
app.include_router(stat_router, prefix="/stats", tags=["Stats"])
app.include_router(save_router, prefix="/saving_throw_progressions", tags=["Saves"])
app.include_router(equipment_router, prefix="/equipment", tags=["Equipment"])
app.include_router(skill_router, prefix="/skills", tags=["Skills"])
app.include_router(money_router, prefix="/money_values", tags=["Money"])
app.include_router(money_router, prefix="/character_money", tags=["Character Money"])
app.include_router(language_router, prefix="/languages", tags=["Languages"])

origins = [
    'http://localhost',
    'http://localhost:3000',
    'http://localhost:5173',
    'https://pathforger.netlify.app'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*']
)

@app.get("/")
def root():
    return {"message": "Hello World"}


# Security dependency
security = HTTPBearer()

def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SUPABASE_SECRET_KEY,
            audience=["authenticated"],
            algorithms=[JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def check_current_credentials(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    token = credentials.credentials
    payload = verify_token(token)
    return payload

@app.get("/characters/")
def get_characters(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], session: Session = Depends(get_session)):
    payload = check_current_credentials(credentials)  # Get user info from the token
    user_id = payload["sub"]  # Extract the `sub` from the JWT payload, which is the user's `uid`

    # Query the characters for the authenticated user (user_id)
    characters = session.exec(select(Character).where(Character.user_id == user_id)).all()

    return characters










@app.post("/characters/")
def create_character(character: Character, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], session: Session = Depends(get_session)):
    payload = check_current_credentials(credentials)  # Get user info from the token
    user_id = payload["sub"]  # Extract user_id from the token
    
    # Assign the user_id to the character
    character.user_id = user_id  # Link the character with the authenticated user
    
    session.add(character)
    session.commit()
    session.refresh(character)
    return character

@app.get("/characters/{character_id}", response_model=Character)
def read_character(character_id: int, session: Session = Depends(get_session)):
    character = session.exec(select(Character).where(Character.id == character_id)).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@app.put("/characters/{character_id}", response_model=Character)
def update_character(
    character_id: int,
    character_update: Character,  # The updated character data will be provided in the request body
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Session = Depends(get_session)
):
    payload = check_current_credentials(credentials)  # Get user info from the token
    user_id = payload["sub"]  # Extract the `sub` (user ID) from the JWT payload

    # Retrieve the character by its ID
    character = session.get(Character, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    # Ensure the character belongs to the authenticated user
    if character.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can only update your own characters")

    # Update the character's fields
    for key, value in character_update.dict(exclude_unset=True).items():
        setattr(character, key, value)

    session.commit()
    session.refresh(character)
    return character


@app.delete("/characters/{character_id}")
def delete_character(
    character_id: int,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Session = Depends(get_session)
):
    payload = check_current_credentials(credentials)  # Get user info from the token
    user_id = payload["sub"]  # Extract the `sub` (user ID) from the JWT payload

    # Retrieve the character by its ID
    character = session.get(Character, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    # Ensure the character belongs to the authenticated user
    if character.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can only delete your own characters")

    # Delete the character
    session.delete(character)
    session.commit()
    return {"message": "Character deleted successfully"}

# Retrieve all races
@app.get("/races/", response_model=List[Race])
def read_all_races(session: Session = Depends(get_session)):
    races = session.exec(select(Race)).all()
    return races

# Retrieve all characters
@app.get("/characters/", response_model=List[Character])
def read_all_characters(session: Session = Depends(get_session)):
    characters = session.exec(select(Character)).all()
    return characters

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
