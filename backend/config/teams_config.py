import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from backend/.env explicitly
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

class TeamsConfig:
    # Microsoft Teams configuration
    CLIENT_ID = os.getenv("TEAMS_CLIENT_ID")
    CLIENT_SECRET = os.getenv("TEAMS_CLIENT_SECRET")
    TENANT_ID = os.getenv("TEAMS_TENANT_ID")
    
    # Teams app URLs
    APP_ID = os.getenv("TEAMS_APP_ID")
    
    # Required permissions
    REQUIRED_PERMISSIONS = [
        "TeamsActivity.Send",
        "TeamsActivity.ReadWrite.All",
        "User.Read",
        "User.ReadBasic.All"
    ]
    
    # Redirect URIs
    REDIRECT_URI = os.getenv("TEAMS_REDIRECT_URI", "https://your-app-url.com/auth/teams")
    
    # Microsoft Graph API endpoints
    GRAPH_API_BASE = "https://graph.microsoft.com/v1.0"
    
    # Teams app manifest configuration
    MANIFEST_VERSION = "1.11"
    SHORT_NAME = os.getenv("TEAMS_APP_SHORT_NAME", "AI Storyteller")
    FULL_NAME = os.getenv("TEAMS_APP_FULL_NAME", "AI Storyteller")
    DESCRIPTION = os.getenv("TEAMS_APP_DESCRIPTION", "AI-powered storytelling application")
