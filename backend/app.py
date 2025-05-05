# backend/app.py

import os
import io # Needed for sending blob data as files
import requests
from flask import Flask, request, jsonify, send_file, abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import openai
from azure.cognitiveservices.speech import (
    SpeechConfig, SpeechSynthesizer, AudioDataStream, ResultReason, CancellationReason,
    SpeechSynthesisOutputFormat
)
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient # Added for Azure Blob Storage

# Load environment variables from .env file (especially for local development)
load_dotenv()

# --- Flask App Initialization ---
app = Flask(__name__)

# --- Database Configuration ---
# Use DATABASE_URL from environment variable. Default to a local file if not set.
# When running in Azure Container Apps with volume mount, set DATABASE_URL to 'sqlite:////data/stories.db'
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///local_stories.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable modification tracking
db = SQLAlchemy(app)

# --- Database Model ---
class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    # We won't store image/audio URLs directly in the DB for this implementation
    # We will retrieve them from blob storage based on the story ID

    def __repr__(self):
        return f'<Story {self.id}: {self.title}>'

# Create database tables if they don't exist
# Needs application context to work
with app.app_context():
    db.create_all()
    print(f"Database initialized at: {DATABASE_URL}")

# --- OpenAI Configuration ---
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    print("Warning: OPENAI_API_KEY environment variable not set.")

# --- Azure Speech Configuration ---
SPEECH_KEY = os.environ.get("AZURE_SPEECH_KEY")
SPEECH_REGION = os.environ.get("AZURE_SPEECH_REGION")
if not SPEECH_KEY or not SPEECH_REGION:
    print("Warning: AZURE_SPEECH_KEY or AZURE_SPEECH_REGION environment variable not set. Speech synthesis will fail.")
    speech_config = None
else:
    speech_config = SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    # Set the output format for audio generation if desired (e.g., MP3)
    speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)

# --- Azure Blob Storage Configuration ---
AZURE_STORAGE_CONNECTION_STRING = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
if not AZURE_STORAGE_CONNECTION_STRING:
    print("Warning: AZURE_STORAGE_CONNECTION_STRING environment variable not set. Blob storage operations will fail.")
    blob_service_client = None
else:
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        print("Successfully connected to Azure Blob Storage.")
        # You might want to ensure containers exist here for local testing,
        # but in Azure, it's better to create them via Portal/CLI/IaC.
        # Example (handle exceptions if container already exists):
        # try: blob_service_client.create_container("stories") except Exception: pass
        # try: blob_service_client.create_container("images") except Exception: pass
        # try: blob_service_client.create_container("audio") except Exception: pass
    except Exception as e:
        print(f"Error connecting to Azure Blob Storage: {e}")
        blob_service_client = None

# === Helper Functions for Blob Storage ===

def upload_blob_data(container_name: str, blob_name: str, data: bytes):
    """Uploads bytes data to a specific blob in a container."""
    if not blob_service_client:
        print(f"Error: Cannot upload {blob_name} to {container_name}. Blob service client not initialized.")
        return None # Indicate failure
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(data, overwrite=True) # Overwrite if exists
        print(f"Uploaded {blob_name} to container {container_name}.")
        # Return the blob name or URL if needed, here returning True for success
        return True
    except Exception as e:
        print(f"Error uploading blob {blob_name} to container {container_name}: {e}")
        return None # Indicate failure

def download_blob_data(container_name: str, blob_name: str) -> bytes | None:
    """Downloads data from a specific blob in a container."""
    if not blob_service_client:
        print(f"Error: Cannot download {blob_name} from {container_name}. Blob service client not initialized.")
        return None
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        if not blob_client.exists():
            print(f"Error: Blob {blob_name} not found in container {container_name}.")
            return None
        download_stream = blob_client.download_blob()
        data = download_stream.readall()
        print(f"Downloaded {blob_name} from container {container_name}.")
        return data
    except Exception as e:
        print(f"Error downloading blob {blob_name} from container {container_name}: {e}")
        return None

# === API Endpoints ===

@app.route('/')
def home():
    return "AI Storyteller Backend is running!"

@app.route('/stories', methods=['GET'])
def get_stories():
    """Returns a list of all stories (ID and Title)."""
    stories = Story.query.all()
    return jsonify([{"id": story.id, "title": story.title} for story in stories])

@app.route('/stories/<int:story_id>', methods=['GET'])
def get_story_details(story_id):
    """Returns details for a specific story (ID, Title, Text)."""
    story = Story.query.get_or_404(story_id)
    return jsonify({"id": story.id, "title": story.title, "text": story.text})

@app.route('/generate_story', methods=['POST'])
def generate_story_route():
    """Generates a story based on a topic using OpenAI."""
    if not openai.api_key:
         return jsonify({"error": "OpenAI API key not configured"}), 500

    data = request.get_json()
    if not data or 'topic' not in data:
        return jsonify({"error": "Missing 'topic' in request body"}), 400
    topic = data['topic']

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative storyteller."},
                {"role": "user", "content": f"Write a short story about: {topic}"}
            ]
        )
        story_text = response.choices[0].message.content.strip()

        # Save basic info to DB
        new_story = Story(title=topic, text=story_text)
        db.session.add(new_story)
        db.session.commit() # Commit to get the new story's ID

        story_id = new_story.id
        print(f"Generated story with ID: {story_id}")

        # Define blob details
        blob_name = f"{story_id}.txt"
        container_name = "stories"

        # Upload the full story text to blob storage
        upload_success = upload_blob_data(container_name, blob_name, story_text.encode('utf-8')) # Encode string to bytes

        if not upload_success:
             # Log error but maybe still return the story? Or return an error?
             print(f"Warning: Failed to upload story text for ID {story_id} to blob storage.")
             # Decide on behaviour - here we still return success as the story is in the DB
             # return jsonify({"error": "Failed to save story text to blob storage"}), 500

        # Return story details
        return jsonify({"id": story_id, "title": topic, "text": story_text}), 201 # 201 Created

    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        print(f"Error generating story: {e}")
        db.session.rollback() # Rollback DB transaction on error
        return jsonify({"error": "An unexpected error occurred during story generation."}), 500

@app.route('/stories/<int:story_id>/generate_image', methods=['POST'])
def generate_image_route(story_id):
    """Generates an image for a story using DALL-E and saves to Blob Storage."""
    story = Story.query.get_or_404(story_id) # Ensure story exists

    if not openai.api_key:
         return jsonify({"error": "OpenAI API key not configured"}), 500

    # Use the story title or a snippet of text as the prompt
    prompt = f"An illustration for the story titled '{story.title}'. {story.text[:200]}" # Limit prompt length

    try:
        image_response = openai.images.generate(
            model="dall-e-3", # Or dall-e-3 if available/preferred
            prompt=prompt,
            n=1,
            size="1024x1024" # Or other supported sizes
        )
        image_url = image_response.data[0].url

        # --- Download image data from DALL-E URL ---
        try:
            image_data_response = requests.get(image_url, stream=True, timeout=30) # Add timeout
            image_data_response.raise_for_status() # Check for download errors (4xx, 5xx)
            image_data = image_data_response.content # Get image bytes
        except requests.exceptions.RequestException as e:
             print(f"Error downloading image from DALL-E url {image_url}: {e}")
             return jsonify({"error": "Failed to download image from DALL-E"}), 500

        # --- Upload image data to Blob Storage ---
        blob_name = f"{story_id}.png" # Assuming DALL-E returns PNG, adjust if needed
        container_name = "images"
        upload_success = upload_blob_data(container_name, blob_name, image_data)

        if not upload_success:
             return jsonify({"error": "Failed to upload image to storage"}), 500

        print(f"Image generated and stored in blob storage for story ID: {story_id}")
        # Return success message. Client will fetch using the GET endpoint.
        return jsonify({"message": "Image generated and stored successfully"}), 200

    except openai.OpenAIError as e:
        print(f"OpenAI API error during image generation: {e}")
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        print(f"Error generating image: {e}")
        return jsonify({"error": "An unexpected error occurred during image generation."}), 500

@app.route('/stories/<int:story_id>/generate_audio', methods=['POST'])
def generate_audio_route(story_id):
    """Generates audio for a story using Azure Speech and saves to Blob Storage."""
    story = Story.query.get_or_404(story_id) # Ensure story exists

    if not speech_config:
        return jsonify({"error": "Azure Speech service not configured"}), 500

    # Use a None audio config to get the data as a memory stream (byte array)
    speech_synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    # Synthesize the full story text
    result = speech_synthesizer.speak_text_async(story.text).get() # Use async and get result

    # --- Process and Upload Audio ---
    if result.reason == ResultReason.SynthesizingAudioCompleted:
        audio_data = result.audio_data # This is the byte array of the audio
        print(f"Successfully synthesized audio for story ID: {story_id}, data length: {len(audio_data)}")

        # --- Upload audio data to Blob Storage ---
        blob_name = f"{story_id}.mp3" # Based on SpeechSynthesisOutputFormat configured earlier
        container_name = "audio"
        upload_success = upload_blob_data(container_name, blob_name, audio_data)

        if not upload_success:
             return jsonify({"error": "Failed to upload audio to storage"}), 500

        print(f"Audio stored in blob storage for story ID: {story_id}")
        # Return success message. Client will fetch using the GET endpoint.
        return jsonify({"message": "Audio generated and stored successfully"}), 200

    elif result.reason == ResultReason.Canceled:
        cancellation = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation.reason}")
        if cancellation.reason == CancellationReason.Error:
            print(f"Error details: {cancellation.error_details}")
        return jsonify({"error": f"Speech synthesis canceled: {cancellation.reason}", "details": cancellation.error_details}), 500
    else:
         print(f"Unknown speech synthesis result reason: {result.reason}")
         return jsonify({"error": "Unknown error during speech synthesis"}), 500

@app.route('/stories/<int:story_id>/image', methods=['GET'])
def get_image_route(story_id):
    """Retrieves the story's image from Azure Blob Storage."""
    # Optional: Check if story exists in DB first
    # Story.query.get_or_404(story_id)

    blob_name = f"{story_id}.png" # Use consistent naming
    container_name = "images"
    image_data = download_blob_data(container_name, blob_name)

    if image_data is None:
        # If the blob doesn't exist or download failed
        abort(404, description=f"Image not found for story {story_id}.")

    # Send the file data from memory
    return send_file(
        io.BytesIO(image_data),
        mimetype='image/png', # Adjust mimetype if necessary
        as_attachment=False, # Display inline in browser if possible
        download_name=f'story_{story_id}_image.png' # Suggested filename if user saves
    )

@app.route('/stories/<int:story_id>/audio', methods=['GET'])
def get_audio_route(story_id):
    """Retrieves the story's audio from Azure Blob Storage."""
    # Optional: Check if story exists in DB first
    # Story.query.get_or_404(story_id)

    blob_name = f"{story_id}.mp3" # Use consistent naming
    container_name = "audio"
    audio_data = download_blob_data(container_name, blob_name)

    if audio_data is None:
         abort(404, description=f"Audio not found for story {story_id}.")

    # Send the file data from memory
    return send_file(
        io.BytesIO(audio_data),
        mimetype='audio/mpeg', # Mimetype for MP3
        as_attachment=False, # Play inline if possible
        download_name=f'story_{story_id}_audio.mp3'
    )

@app.route('/stories/<int:story_id>/text', methods=['GET'])
def get_text_route(story_id):
     """Retrieves the story's full text, preferably from Blob Storage as source of truth."""
     # Option 1: Get from Blob (ensures consistency with generated assets)
     blob_name = f"{story_id}.txt"
     container_name = "stories"
     text_data_bytes = download_blob_data(container_name, blob_name)

     if text_data_bytes is None:
         # Fallback: Try getting from DB if blob fails? Or just 404?
         # story = Story.query.get(story_id)
         # if story:
         #     print(f"Warning: Text blob not found for story {story_id}, serving from DB.")
         #     return story.text, 200, {'Content-Type': 'text/plain; charset=utf-8'}
         # else:
         #     abort(404, description=f"Story text not found in Blob or DB for story {story_id}.")
        abort(404, description=f"Story text not found in Blob Storage for story {story_id}.")


     # Decode bytes to string and return with correct Content-Type
     return text_data_bytes.decode('utf-8'), 200, {'Content-Type': 'text/plain; charset=utf-8'}

     # # Option 2: Get directly from DB (Simpler if DB text is always the primary source)
     # story = Story.query.get_or_404(story_id)
     # return story.text, 200, {'Content-Type': 'text/plain; charset=utf-8'}


# --- Main Execution ---
if __name__ == '__main__':
    # Use Gunicorn for production, this is for local development `python app.py`
    # Make sure to set HOST='0.0.0.0' to be reachable outside Docker if running locally this way
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port) # debug=True enables auto-reload, turn off for production