# backend/config/config.py

import os
from dotenv import load_dotenv
import sys # For printing to stderr
from backend.extensions import db

# Determine the base directory of the 'backend' folder
backend_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
dotenv_path = os.path.join(backend_dir, '.env')

# --- .env Loading ---
# This still runs, useful for local development where .env might define DATABASE_URL
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
    SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'a_very_strong_default_secret_key_for_dev_only' # Use strong secret in production env var
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')

    # --- Database ---
    # ONLY look for external DATABASE_URL or SQLALCHEMY_DATABASE_URI set in the environment
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              os.environ.get('SQLALCHEMY_DATABASE_URI')

    # CRITICAL: Ensure one of the above is set in the deployment environment (ACA)
    if not SQLALCHEMY_DATABASE_URI:
        print("FATAL ERROR: DATABASE_URL or SQLALCHEMY_DATABASE_URI not set in environment!", file=sys.stderr)
        # In a real app, you might want to raise an error here to prevent startup without a DB
        # raise ValueError("Database connection string not configured in environment.")
        # For now, we'll let it potentially fail later if code tries to use db without URI

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Configure connection timeout settings for PostgreSQL
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'connect_timeout': 30,  # Increased to 30 seconds
            'options': '-c statement_timeout=30000 -c tcp_keepalives_idle=60 -c tcp_keepalives_interval=10 -c tcp_keepalives_count=5'
        },
        'pool_size': 5,
        'max_overflow': 10,
        'pool_timeout': 30,
        'pool_recycle': 3600
    }

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
    AZURE_FILE_SHARE_NAME = os.environ.get('AZURE_FILE_SHARE_NAME', 'story-audio') # Keep if used

    # --- OpenAI (if using the direct OpenAI API as well) ---
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

    # Executor settings
    EXECUTOR_TYPE = 'thread'
    EXECUTOR_MAX_WORKERS = int(os.environ.get('EXECUTOR_MAX_WORKERS', 5))

    # --- Log effective settings ---
    # Changed log for database URI
    print(f"[Config] DATABASE_URL set in environment: {bool(os.environ.get('DATABASE_URL'))}", file=sys.stderr)
    print(f"[Config] SQLALCHEMY_DATABASE_URI set in environment: {bool(os.environ.get('SQLALCHEMY_DATABASE_URI'))}", file=sys.stderr)
    print(f"[Config] Effective DB URI will be used by SQLAlchemy: {bool(SQLALCHEMY_DATABASE_URI)}", file=sys.stderr)
    print(f"[Config] AZURE_OPENAI_ENDPOINT set: {bool(AZURE_OPENAI_ENDPOINT)}", file=sys.stderr)
    print(f"[Config] AZURE_SPEECH_REGION set: {bool(AZURE_SPEECH_REGION)}", file=sys.stderr)
    print(f"[Config] AZURE_STORAGE_CONNECTION_STRING set: {bool(AZURE_STORAGE_CONNECTION_STRING)}", file=sys.stderr)
    print(f"[Config] Using Image Container: {AZURE_IMAGES_CONTAINER_NAME}", file=sys.stderr)
    print(f"[Config] Using Audio Container: {AZURE_AUDIO_CONTAINER_NAME}", file=sys.stderr)
    print(f"[Config] Using File Share (optional): {AZURE_FILE_SHARE_NAME}", file=sys.stderr)
    print("Config class initialized.", file=sys.stderr)