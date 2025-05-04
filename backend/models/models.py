# models.py
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///stories.db")
# Make sure parent directory exists when using mounted path
if DATABASE_URL.startswith("sqlite:////data/"):
    os.makedirs("/data", exist_ok=True)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Story(Base):
    __tablename__ = "stories"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    prompt = Column(Text)
    # Store blob references instead of actual content
    story_blob_ref = Column(String)
    image_blob_ref = Column(String)
    audio_blob_ref = Column(String)

# Create the tables
Base.metadata.create_all(bind=engine)
 