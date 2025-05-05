# backend/app.py

import os
import io
import requests
import logging
from flask import Flask, request, jsonify, send_file, abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import openai
from azure.cognitiveservices.speech import (
    SpeechConfig, SpeechSynthesizer, AudioDataStream, ResultReason, CancellationReason,
    SpeechSynthesisOutputFormat
)
from azure.storage.blob import BlobServiceClient, ContainerClient
from azure.core.exceptions import ResourceExistsError, HttpResponseError

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Configuration
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///local_stories.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Story {self.id}: {self.title}>'

# Initialize database
with app.app_context():
    db.create_all()
    logger.info(f"Database initialized at: {DATABASE_URL}")

# Azure Blob Storage Configuration
blob_service_client = None
try:
    connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    if connection_string:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        # Verify required containers exist
        required_containers = ["stories", "images", "audio"]
        for container_name in required_containers:
            container_client = blob_service_client.get_container_client(container_name)
            if not container_client.exists():
                logger.warning(f"Container {container_name} does not exist, creating...")
                container_client.create_container()
        logger.info("Azure Blob Storage initialized successfully")
except Exception as e:
    logger.error(f"Azure Blob Storage initialization failed: {str(e)}")
    blob_service_client = None

# OpenAI Configuration
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Azure Speech Configuration
speech_config = None
try:
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")
    if speech_key and speech_region:
        speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
        speech_config.set_speech_synthesis_output_format(
            SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
        )
        logger.info("Azure Speech Service configured")
except Exception as e:
    logger.error(f"Azure Speech Service configuration failed: {str(e)}")

# Storage Helper Functions
def upload_blob(container_name, blob_name, data):
    if not blob_service_client:
        logger.error("Blob service client not initialized")
        return False
    
    try:
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()
            
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data, overwrite=True)
        logger.info(f"Uploaded {blob_name} to {container_name}")
        return True
    except ResourceExistsError:
        return True
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        return False

def download_blob(container_name, blob_name):
    if not blob_service_client:
        return None
    
    try:
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        if not blob_client.exists():
            return None
            
        stream = blob_client.download_blob()
        return stream.readall()
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        return None

# API Endpoints
@app.route('/health')
def health_check():
    status = {
        "database": "ok" if db.session.execute("SELECT 1").scalar() else "error",
        "blob_storage": "ok" if blob_service_client else "error",
        "speech_service": "ok" if speech_config else "error",
        "openai": "ok" if openai.api_key else "error"
    }
    return jsonify(status), 200 if all(v == "ok" for v in status.values()) else 500

@app.route('/stories', methods=['GET'])
def get_stories():
    stories = Story.query.all()
    return jsonify([{"id": s.id, "title": s.title} for s in stories])

@app.route('/generate_story', methods=['POST'])
def generate_story():
    if not request.json or 'topic' not in request.json:
        return jsonify({"error": "Missing topic"}), 400
    
    topic = request.json['topic']
    
    try:
        # Generate story text
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative storyteller."},
                {"role": "user", "content": f"Write a short story about: {topic}"}
            ]
        )
        story_text = response.choices[0].message.content.strip()
        
        # Save to database
        story = Story(title=topic, text=story_text)
        db.session.add(story)
        db.session.commit()
        
        # Save to blob storage
        if not upload_blob("stories", f"{story.id}.txt", story_text.encode('utf-8')):
            logger.warning(f"Failed to save story {story.id} to blob storage")
        
        return jsonify({
            "id": story.id,
            "title": story.title,
            "text": story_text
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Story generation failed: {str(e)}")
        return jsonify({"error": "Story generation failed"}), 500

@app.route('/stories/<int:story_id>/generate_image', methods=['POST'])
def generate_image(story_id):
    story = Story.query.get_or_404(story_id)
    
    try:
        # Generate image
        response = openai.images.generate(
            prompt=f"Illustration for: {story.text[:200]}",
            model="dall-e-3",
            size="1024x1024"
        )
        image_url = response.data[0].url
        
        # Download and store image
        image_data = requests.get(image_url).content
        if not upload_blob("images", f"{story_id}.png", image_data):
            return jsonify({"error": "Failed to store image"}), 500
            
        return jsonify({"message": "Image generated successfully"}), 200
        
    except Exception as e:
        logger.error(f"Image generation failed: {str(e)}")
        return jsonify({"error": "Image generation failed"}), 500

@app.route('/stories/<int:story_id>/image', methods=['GET'])
def get_image(story_id):
    image_data = download_blob("images", f"{story_id}.png")
    if not image_data:
        abort(404)
        
    return send_file(
        io.BytesIO(image_data),
        mimetype='image/png',
        download_name=f'story_{story_id}_image.png'
    )

@app.route('/stories/<int:story_id>/generate_audio', methods=['POST'])
def generate_audio(story_id):
    story = Story.query.get_or_404(story_id)
    
    if not speech_config:
        return jsonify({"error": "Speech service not configured"}), 500
        
    try:
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)
        result = synthesizer.speak_text_async(story.text).get()
        
        if result.reason == ResultReason.SynthesizingAudioCompleted:
            if not upload_blob("audio", f"{story_id}.mp3", result.audio_data):
                return jsonify({"error": "Failed to store audio"}), 500
            return jsonify({"message": "Audio generated successfully"}), 200
        else:
            logger.error(f"Speech synthesis failed: {result.cancellation_details.error_details}")
            return jsonify({"error": "Audio generation failed"}), 500
    except Exception as e:
        logger.error(f"Audio generation failed: {str(e)}")
        return jsonify({"error": "Audio generation failed"}), 500

@app.route('/stories/<int:story_id>/audio', methods=['GET'])
def get_audio(story_id):
    audio_data = download_blob("audio", f"{story_id}.mp3")
    if not audio_data:
        abort(404)
        
    return send_file(
        io.BytesIO(audio_data),
        mimetype='audio/mpeg',
        download_name=f'story_{story_id}_audio.mp3'
    )

@app.route('/stories/<int:story_id>/text', methods=['GET'])
def get_text(story_id):
    text_data = download_blob("stories", f"{story_id}.txt")
    if text_data:
        return text_data.decode('utf-8'), 200, {'Content-Type': 'text/plain; charset=utf-8'}
    
    # Fallback to database
    story = Story.query.get(story_id)
    if story:
        return story.text, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    
    abort(404)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)