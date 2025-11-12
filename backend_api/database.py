
# database.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

# --- DATABASE CONFIGURATION ---
# For a real project, use environment variables for this!
DATABASE_URL = "postgresql://postgres:xctJ2H7xYO7dfvsO@db.esqhydhrpxjmkrydhdek.supabase.co:5432/postgres" # IMPORTANT: Update with your DB URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- DATABASE MODEL ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # --- ADD THIS LINE ---
    history = relationship("SearchHistory", back_populates="owner")

class SearchHistory(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    # We'll save the first 100 chars of the prompt as a title
    prompt_title = Column(String(100)) 
    summary = Column(Text)
    # Store the hyperlinks as a simple string for now
    hyperlinks_json = Column(Text) 
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    # This is the link to the User table
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="history")


# --- DEPENDENCY ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
