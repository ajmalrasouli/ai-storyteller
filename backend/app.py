# app.py
import os
import io
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import models
from models import Story
from sqlalchemy.orm import Session
import openai
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig, ResultReason
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import base64
import uuid
import json
from storage import AzureStorageManager  # Import the new storage manager

# Load environment variables
load_dotenv()

# Initialize storage manager
storage_manager = AzureStorageManager()

# Set up OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_type = os.getenv("OPENAI_API_TYPE", "azure")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION", "2023-05-15")

# Set up Azure Speech
speech_key = os.getenv("SPEECH_KEY")
speech_region = os.getenv("SPEECH_REGION", "eastus")
speech_config = SpeechConfig(subscription=speech_key, region=speech_region)

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class StoryRequest(BaseModel):
    prompt: str
    
# Helper to get database session
def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to generate story
async def generate_story(prompt):
    response = openai.ChatCompletion.create(
        engine="gpt-4",
        messages=[
            {"role": "system", "content": "You are a creative storyteller."},
            {"role": "user", "content": f"Generate a short story based on: {prompt}"}
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content

# Function to generate image
async def generate_image(prompt):
    response = openai.Image.create(
        prompt=f"Create an image for a story about: {prompt}",
        n=1,
        size="1024x1024"
    )
    image_url = response.data[0].url
    # Download image from URL
    import requests
    image_data = requests.get(image_url).content
    return image_data

# Function to generate speech
async def generate_speech(text):
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
    audio_config = AudioOutputConfig(filename="temp_audio.wav")
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    result = synthesizer.speak_text_async(text).get()
    if result.reason == ResultReason.SynthesizingAudioCompleted:
        # Read the audio file
        with open("temp_audio.wav", "rb") as audio_file:
            audio_data = audio_file.read()
        # Clean up
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")
        return audio_data
    else:
        raise Exception("Speech synthesis failed")

@app.post("/api/stories")
async def create_story(request: StoryRequest, background_tasks: BackgroundTasks, db: Session = next(get_db())):
    # Generate story
    story_text = await generate_story(request.prompt)
    
    # Extract title from the first line
    title = story_text.strip().split("\n")[0].replace("#", "").strip()
    if not title or len(title) > 100:
        title = f"Story about {request.prompt[:50]}..."
    
    # Create a new story entry
    story_id = str(uuid.uuid4())
    db_story = Story(
        title=title,
        prompt=request.prompt,
        story_blob_ref="",
        image_blob_ref="",
        audio_blob_ref=""
    )
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    
    # Upload story text to blob storage
    story_blob_ref = storage_manager.upload_story_text(story_text, db_story.id)
    
    # Generate and upload image
    image_data = await generate_image(request.prompt)
    image_blob_ref = storage_manager.upload_image(image_data, db_story.id)
    
    # Generate and upload audio
    audio_data = await generate_speech(story_text)
    audio_blob_ref = storage_manager.upload_audio(audio_data, db_story.id)
    
    # Update story with blob references
    db_story.story_blob_ref = story_blob_ref
    db_story.image_blob_ref = image_blob_ref
    db_story.audio_blob_ref = audio_blob_ref
    db.commit()
    
    return {
        "id": db_story.id,
        "title": title,
        "prompt": request.prompt,
        "story": story_text,
        "image": f"/api/stories/{db_story.id}/image",
        "audio": f"/api/stories/{db_story.id}/audio"
    }

@app.get("/api/stories")
async def get_stories(db: Session = next(get_db())):
    stories = db.query(Story).all()
    return [{"id": story.id, "title": story.title, "prompt": story.prompt} for story in stories]

@app.get("/api/stories/{story_id}")
async def get_story(story_id: int, db: Session = next(get_db())):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # Get story text from blob
    story_text = storage_manager.get_story_text(story.story_blob_ref)
    
    return {
        "id": story.id,
        "title": story.title,
        "prompt": story.prompt,
        "story": story_text,
        "image": f"/api/stories/{story.id}/image",
        "audio": f"/api/stories/{story.id}/audio"
    }

@app.get("/api/stories/{story_id}/image")
async def get_story_image(story_id: int, db: Session = next(get_db())):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story or not story.image_blob_ref:
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Get image from blob
    image_data = storage_manager.get_image(story.image_blob_ref)
    
    return StreamingResponse(io.BytesIO(image_data), media_type="image/png")

@app.get("/api/stories/{story_id}/audio")
async def get_story_audio(story_id: int, db: Session = next(get_db())):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story or not story.audio_blob_ref:
        raise HTTPException(status_code=404, detail="Audio not found")
    
    # Get audio from blob
    audio_data = storage_manager.get_audio(story.audio_blob_ref)
    
    return StreamingResponse(io.BytesIO(audio_data), media_type="audio/mpeg")