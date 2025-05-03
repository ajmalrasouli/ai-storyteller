import os
from dotenv import load_dotenv
from pathlib import Path

# Try to load environment variables from backend/.env, but continue if not found
# This ensures we fall back to system environment variables in Docker
try:
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    print(f"Tried to load .env from {env_path}")
except Exception as e:
    print(f"No .env file found or error loading it: {str(e)}")
    print("Will use system environment variables instead")

class TeamsConfig:
    # Microsoft Teams configuration
    CLIENT_ID = os.getenv("TEAMS_CLIENT_ID")
    CLIENT_SECRET = os.getenv("TEAMS_CLIENT_SECRET")
    TENANT_ID = os.getenv("TEAMS_TENANT_ID")
    
    # Bot configuration
    BOT_ID = os.getenv("BOT_ID")
    BOT_PASSWORD = os.getenv("BOT_PASSWORD")
    
    # Teams app URLs
    APP_ID = os.getenv("TEAMS_APP_ID")
    WEBSITE_URL = os.getenv("WEBSITE_URL", "https://proud-water-076db370f.6.azurestaticapps.net")
    
    # Required permissions
    REQUIRED_PERMISSIONS = [
        "TeamsActivity.Send",
        "TeamsActivity.ReadWrite.All",
        "User.Read",
        "User.ReadBasic.All"
    ]
    
    # Authentication configuration
    OAUTH_AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
    OAUTH_SCOPE = ["https://graph.microsoft.com/.default"]
    TOKEN_CACHE_FILE = "teams_token_cache.json"
    REDIRECT_URI = os.getenv("TEAMS_REDIRECT_URI", f"{WEBSITE_URL}/auth/teams")
    
    # Microsoft Graph API endpoints
    GRAPH_API_BASE = "https://graph.microsoft.com/v1.0"
    
    # Teams app manifest configuration
    MANIFEST_VERSION = "1.16"
    SHORT_NAME = os.getenv("TEAMS_APP_SHORT_NAME", "Storyteller")
    FULL_NAME = os.getenv("TEAMS_APP_FULL_NAME", "AI Storyteller Bot")
    DESCRIPTION = os.getenv("TEAMS_APP_DESCRIPTION", "Create engaging children's stories using AI.")
