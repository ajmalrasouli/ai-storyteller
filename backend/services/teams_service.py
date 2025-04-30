import requests
from flask import current_app
from .teams_config import TeamsConfig
import jwt
from datetime import datetime, timedelta


class TeamsService:
    def __init__(self):
        self.config = TeamsConfig()
        
    def get_auth_url(self):
        """Generate authorization URL for Teams authentication"""
        auth_url = f"https://login.microsoftonline.com/{self.config.TENANT_ID}/oauth2/v2.0/authorize"
        params = {
            'client_id': self.config.CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': self.config.REDIRECT_URI,
            'response_mode': 'query',
            'scope': ' '.join(self.config.REQUIRED_PERMISSIONS),
            'state': self._generate_state()
        }
        return f"{auth_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    
    def get_access_token(self, auth_code):
        """Exchange authorization code for access token"""
        token_url = f"https://login.microsoftonline.com/{self.config.TENANT_ID}/oauth2/v2.0/token"
        data = {
            'client_id': self.config.CLIENT_ID,
            'client_secret': self.config.CLIENT_SECRET,
            'code': auth_code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.config.REDIRECT_URI,
            'scope': ' '.join(self.config.REQUIRED_PERMISSIONS)
        }
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        return response.json()
    
    def send_message_to_team(self, team_id, message):
        """Send a message to a specific team"""
        url = f"{self.config.GRAPH_API_BASE}/teams/{team_id}/channels/general/messages"
        headers = {
            'Authorization': f'Bearer {self._get_access_token()}',
            'Content-Type': 'application/json'
        }
        data = {
            'body': {
                'content': message
            }
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def _get_access_token(self):
        """Get access token from cache or refresh if needed"""
        # Implement token caching and refresh logic here
        # This is a placeholder - you'll need to implement proper token management
        return current_app.config.get('TEAMS_ACCESS_TOKEN')
    
    def _generate_state(self):
        """Generate a secure state parameter"""
        return jwt.encode(
            {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow()
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
