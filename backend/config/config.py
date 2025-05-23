import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from backend/.env explicitly
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///stories.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Azure OpenAI configuration
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo")
    AZURE_OPENAI_API_VERSION = "2024-02-01"
    AZURE_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")

    # Azure Speech configuration
    AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
    AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

    # Azure Blob Storage configuration
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    AZURE_STORAGE_CONTAINER_STORIES = os.getenv("AZURE_STORAGE_CONTAINER_STORIES", "stories")
    AZURE_STORAGE_CONTAINER_AUDIO = os.getenv("AZURE_STORAGE_CONTAINER_AUDIO", "audio")
    AZURE_STORAGE_CONTAINER_IMAGES = os.getenv("AZURE_STORAGE_CONTAINER_IMAGES", "images")
    AZURE_STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    AZURE_STORAGE_ACCOUNT_KEY = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")