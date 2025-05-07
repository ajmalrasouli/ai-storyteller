import os
from dotenv import load_dotenv
import sys # For printing to stderr

# Determine the base directory of the 'backend' folder
# __file__ is config/config.py -> dirname is config/ -> parent is backend/
backend_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
dotenv_path = os.path.join(backend_dir, '.env')

print(f"Attempting to load .env from: {dotenv_path}", file=sys.stderr)
if os.path.exists(dotenv_path):
    loaded = load_dotenv(dotenv_path)
    if loaded:
        print(f"Successfully loaded .env file from: {dotenv_path}", file=sys.stderr)
    else:
         print(f"Found .env file but failed to load: {dotenv_path}", file=sys.stderr)
else:
    print(f"Warning: .env file not found at {dotenv_path}. Relying on environment variables set externally.", file=sys.stderr)

class Config:
    print("Initializing Config class...", file=sys.stderr)
    # --- General Flask Settings ---
    SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'a_very_strong_default_secret_key_for_dev_only'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')

    # --- Database ---
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              os.environ.get('SQLALCHEMY_DATABASE_URI') or \
                              f"sqlite:///{os.path.join(backend_dir, 'app.db')}" # Fallback
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Azure OpenAI (Chat/Text) ---
    AZURE_OPENAI_API_KEY = os.environ.get('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_ENDPOINT = os.environ.get('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_DEPLOYMENT_NAME = os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME')
    AZURE_OPENAI_API_VERSION = os.environ.get('AZURE_OPENAI_API_VERSION', "2024-02-01") # Default added

    # --- Azure OpenAI (DALL-E / Images) ---
    AZURE_DALLE_API_KEY = os.environ.get('AZURE_DALLE_API_KEY', AZURE_OPENAI_API_KEY) # Default to same key
    AZURE_DALLE_ENDPOINT = os.environ.get('AZURE_DALLE_ENDPOINT', AZURE_OPENAI_ENDPOINT) # Default to same endpoint
    AZURE_DALLE_DEPLOYMENT_NAME = os.environ.get('AZURE_DALLE_DEPLOYMENT_NAME')
    AZURE_DALLE_API_VERSION = os.environ.get('AZURE_DALLE_API_VERSION') # No default, might differ

    # --- Azure Speech Services ---
    AZURE_SPEECH_KEY = os.environ.get('AZURE_SPEECH_KEY')
    AZURE_SPEECH_REGION = os.environ.get('AZURE_SPEECH_REGION')

    # --- Azure Storage (Blob and File Share) ---
    AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING') or \
                                      os.environ.get('STORAGE_CONNECTION_STRING')
    AZURE_STORAGE_CONTAINER_NAME = os.environ.get('AZURE_STORAGE_CONTAINER_NAME', 'story-images')
    AZURE_FILE_SHARE_NAME = os.environ.get('AZURE_FILE_SHARE_NAME', 'story-audio')

    # --- OpenAI (if using the direct OpenAI API as well) ---
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

    # Executor settings (if you use Flask-Executor)
    EXECUTOR_TYPE = 'thread'
    EXECUTOR_MAX_WORKERS = int(os.environ.get('EXECUTOR_MAX_WORKERS', 5))

    # --- Teams Config (Loaded separately by teams_config.py, but useful to see if needed here) ---
    # You might centralize these here too if preferred
    # TEAMS_CLIENT_ID = os.getenv("TEAMS_CLIENT_ID")
    # BOT_ID = os.getenv("BOT_ID")
    # etc.

    # Simple check to log if critical Azure vars are missing
    print(f"[Config] SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}", file=sys.stderr)
    print(f"[Config] AZURE_OPENAI_ENDPOINT set: {bool(AZURE_OPENAI_ENDPOINT)}", file=sys.stderr)
    print(f"[Config] AZURE_SPEECH_REGION set: {bool(AZURE_SPEECH_REGION)}", file=sys.stderr)
    print(f"[Config] AZURE_STORAGE_CONNECTION_STRING set: {bool(AZURE_STORAGE_CONNECTION_STRING)}", file=sys.stderr)
    print("Config class initialized.", file=sys.stderr)