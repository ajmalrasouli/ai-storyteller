import json
import requests
from flask import current_app
from .teams_config import TeamsConfig

class TeamsBotService:
    def __init__(self):
        self.config = TeamsConfig()
        
    def send_message(self, team_id: str, channel_id: str, message: str):
        """Send a message to a Teams channel"""
        url = f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages"
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
    
    def send_card_message(self, team_id: str, channel_id: str, card_data: dict):
        """Send a rich card message to Teams"""
        url = f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages"
        headers = {
            'Authorization': f'Bearer {self._get_access_token()}',
            'Content-Type': 'application/json'
        }
        data = {
            'body': {
                'contentType': 'application/vnd.microsoft.card.adaptive',
                'content': card_data
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def _get_access_token(self):
        """Get access token from cache or refresh if needed"""
        # This should be implemented with proper token caching and refresh
        # For now, using the client credentials flow
        token_url = f"https://login.microsoftonline.com/{self.config.TENANT_ID}/oauth2/v2.0/token"
        data = {
            'client_id': self.config.CLIENT_ID,
            'client_secret': self.config.CLIENT_SECRET,
            'scope': 'https://graph.microsoft.com/.default',
            'grant_type': 'client_credentials'
        }
        
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        return response.json()['access_token']
    
    def create_adaptive_card(self, title: str, text: str, actions: list = None):
        """Create an adaptive card"""
        card = {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.5",
            "body": [
                {
                    "type": "TextBlock",
                    "text": title,
                    "weight": "Bolder",
                    "size": "Medium"
                },
                {
                    "type": "TextBlock",
                    "text": text,
                    "wrap": True
                }
            ]
        }
        
        if actions:
            card['actions'] = actions
            
        return card
    
    def create_action_buttons(self, buttons: list):
        """Create action buttons for adaptive card"""
        return [
            {
                "type": "Action.Submit",
                "title": button['title'],
                "data": button['data']
            }
            for button in buttons
        ]
