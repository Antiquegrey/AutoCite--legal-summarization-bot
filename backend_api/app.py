# backend_api/app.py
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import traceback
import json               # <-- ADDED: To handle hyperlink serialization
from typing import List   # <-- ADDED: For the new history response model

from . import auth, database, schemas, processing

database.Base.metadata.create_all(bind=database.engine)
app = FastAPI(title="Legal AI Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/signup", response_model=schemas.UserInDB)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = auth.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = database.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = auth.get_user(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# CORE ENDPOINT IS NOW ASYNC
@app.post("/analyze-text/", response_model=schemas.AnalysisResponse)
async def analyze_text(
    request: schemas.TextRequest,
    db: Session = Depends(database.get_db), # <-- ADDED: db session
    current_user: schemas.UserInDB = Depends(auth.get_current_user)
):
    document_text = request.text
    if not document_text:
        raise HTTPException(status_code=400, detail="No text provided.")

    try:
        llm_response = await processing.analyze_legal_text_with_gemini(document_text)
    
    except Exception as e:
        print("---!!! DETAILED ERROR CAUGHT IN /analyze-text/ !!!---")
        print(traceback.format_exc())
        print("---!!! END OF ERROR !!!---")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    if not llm_response:
        raise HTTPException(status_code=500, detail="Failed to get a response from the AI service.")

    summary, hyperlinks = processing.extract_and_hyperlink_citations(llm_response)

    # --- NEW BLOCK TO SAVE HISTORY ---
    # We must do this *before* returning the response
    try:
        # Convert hyperlinks list of dicts to a JSON string to store in DB
        hyperlinks_str = json.dumps(hyperlinks)

        new_history = database.SearchHistory(
            prompt_title=document_text[:100] + "...", # Save first 100 chars
            summary=summary,
            hyperlinks_json=hyperlinks_str,
            owner_id=current_user.id # Link to the logged-in user
        )
        db.add(new_history)
        db.commit()
    except Exception as e:
        # If saving history fails, don't crash the whole request
        # Just print the error and continue
        print("---!!! FAILED TO SAVE HISTORY !!!---")
        print(e)
        print("---!!! END OF HISTORY ERROR !!!---")
    # --- END OF NEW BLOCK ---

    return schemas.AnalysisResponse(summary=summary, hyperlinks=hyperlinks)

# --- NEW ENDPOINT TO GET HISTORY ---
@app.get("/history", response_model=List[schemas.History])
def get_user_history(
    db: Session = Depends(database.get_db),
    current_user: schemas.UserInDB = Depends(auth.get_current_user)
):
    """
    Fetches all history items for the currently logged-in user.
    """
    history = (
        db.query(database.SearchHistory)
        .filter(database.SearchHistory.owner_id == current_user.id)
        .order_by(database.SearchHistory.created_at.desc()) # Show newest first
        .all()
    )
    return history
# --- END OF NEW ENDPOINT ---

@app.get("/")
def root():
    return {"message": "Welcome to the Legal AI Assistant API!"}
