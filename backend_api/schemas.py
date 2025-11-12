from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- BASE SCHEMAS ---

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

# --- HISTORY SCHEMAS (NEW) ---

class HistoryBase(BaseModel):
    prompt_title: str
    summary: str
    hyperlinks_json: str

class History(HistoryBase):
    id: int
    created_at: datetime
    owner_id: int

    # This tells Pydantic to read data from SQLAlchemy models
    class Config:
        from_attributes = True

# --- USER SCHEMA (UPDATED) ---

class UserInDB(UserBase):
    id: int
    hashed_password: str
    history: List[History] = [] # <-- ADDED THIS LINE

    # This tells Pydantic to read data from SQLAlchemy models
    class Config:
        from_attributes = True

# --- TOKEN SCHEMAS ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- ANALYSIS SCHEMAS ---

class TextRequest(BaseModel):
    text: str

class Hyperlink(BaseModel):
    citation_text: str
    url: str

class AnalysisResponse(BaseModel):
    summary: str
    hyperlinks: List[Hyperlink]
