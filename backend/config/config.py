# backend/config/config.py

import os
from dotenv import load_dotenv
import sys # For printing to stderr

# Determine the base directory of the 'backend' folder
# __file__ is config/config.py -> dirname is config/ -> parent is backend/
backend_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
dotenv_path = os.path.join(backend_dir, '.env')

# --- .env Loading ---
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
    # Define a persistent storage path INSIDE the container (to be mounted)
    SQLITE_DB_FOLDER = "/data" # Standard location for mounted data in containers
    SQLITE_DB_PATH = os.path.join(SQLITE_DB_FOLDER, 'app.db')

    # Prioritize external DB URL, fallback to persistent SQLite path inside container
    # USE explicit absolute path for SQLite within container file system
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              os.environ.get('SQLALCHEMY_DATABASE_URI') or \
                              f"sqlite:////{SQLITE_DB_PATH}" # Use //// for absolute path

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- ADD SQLALCHEMY ENGINE OPTIONS for SQLite Timeout ---
    # Only apply these options if we are actually using the SQLite fallback
    # This prevents applying SQLite specific options if DATABASE_URL for PostgreSQL is set
    if SQLALCHEMY_DATABASE_URI.startswith('sqlite:'):
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {
                "timeout": 30  # Increase timeout to 30 seconds (default is 5)
                }
            # Potentially add WAL mode - uncomment if timeout alone isn't enough
            # "execution_options": {"sqlite_journal_mode": "WAL"} # May require app changes too
        }
        print("[Config] Applying SQLite specific engine options (timeout=30).", file=sys.stderr)
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {} # Use empty dict if not SQLite
    # -------------------------------------------------------

    # --- Azure OpenAI (Chat/Text) ---
    AZURE_OPENAI_API_KEY = os.environ.get('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_ENDPOINT = os.environ.get('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_DEPLOYMENT_NAME = os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME')
    AZURE_OPENAI_API_VERSION = os.environ.get('AZURE_OPENAI_API_VERSION', "2024-02-01")

    # --- Azure OpenAI (DALL-E / Images) ---
    AZURE_DALLE_API_KEY = os.environ.get('AZURE_DALLE_API_KEY', AZURE_OPENAI_API_KEY)
    AZURE_DALLE_ENDPOINT = os.environ.get('AZURE_DALLE_ENDPOINT', AZURE_OPENAI_ENDPOINT)
    AZURE_DALLE_DEPLOYMENT_NAME = os.environ.get('AZURE_DALLE_DEPLOYMENT_NAME')
    AZURE_DALLE_API_VERSION = os.environ.get('AZURE_DALLE_API_VERSION')

    # --- Azure Speech Services ---
    AZURE_SPEECH_KEY = os.environ.get('AZURE_SPEECH_KEY')
    AZURE_SPEECH_REGION = os.environ.get('AZURE_SPEECH_REGION')

    # --- Azure Storage ---
    AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING') or \
                                      os.environ.get('STORAGE_CONNECTION_STRING')
    # --- Specific Container/Share Names ---
    AZURE_IMAGES_CONTAINER_NAME = os.environ.get('AZURE_IMAGES_CONTAINER_NAME', 'images')
    AZURE_AUDIO_CONTAINER_NAME = os.environ.get('AZURE_AUDIO_CONTAINER_NAME', 'audio')
    AZURE_FILE_SHARE_NAME = os.environ.get('AZURE_FILE_SHARE_NAME', 'story-audio') # Keep if file share used elsewhere

    # --- OpenAI (if using the direct OpenAI API as well) ---
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

    # Executor settings (if you use Flask-Executor)
    EXECUTOR_TYPE = 'thread'
    EXECUTOR_MAX_WORKERS = int(os.environ.get('EXECUTOR_MAX_WORKERS', 5))

    # --- Log effective settings ---
    print(f"[Config] Effective SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}", file=sys.stderr)
    print(f"[Config] AZURE_OPENAI_ENDPOINT set: {bool(AZURE_OPENAI_ENDPOINT)}", file=sys.stderr)
    print(f"[Config] AZURE_SPEECH_REGION set: {bool(AZURE_SPEECH_REGION)}", file=sys.stderr)
    print(f"[Config] AZURE_STORAGE_CONNECTION_STRING set: {bool(AZURE_STORAGE_CONNECTION_STRING)}", file=sys.stderr)
    print(f"[Config] Using Image Container: {AZURE_IMAGES_CONTAINER_NAME}", file=sys.stderr)
    print(f"[Config] Using Audio Container: {AZURE_AUDIO_CONTAINER_NAME}", file=sys.stderr)
    print(f"[Config] Using File Share (optional): {AZURE_FILE_SHARE_NAME}", file=sys.stderr)
    print("Config class initialized.", file=sys.stderr)