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
    
    # Bot configuration
    BOT_ID = os.getenv("BOT_ID")
    BOT_PASSWORD = os.getenv("BOT_PASSWORD")
    
    # Teams app URLs
    APP_ID = os.getenv("TEAMS_APP_ID")
    WEBSITE_URL = os.getenv("WEBSITE_URL")
    
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
    MANIFEST_VERSION = "1.16"
    SHORT_NAME = os.getenv("TEAMS_APP_SHORT_NAME", "Storyteller")
    FULL_NAME = os.getenv("TEAMS_APP_FULL_NAME", "AI Storyteller Bot")
    DESCRIPTION = os.getenv("TEAMS_APP_DESCRIPTION", "Create engaging children's stories using AI. Just type /storyteller prompt: [Your Prompt] to get started!")
