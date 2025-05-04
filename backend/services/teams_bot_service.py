import json
import requests
from flask import current_app
from config.teams_config import TeamsConfig
from botbuilder.core import BotFrameworkAdapter, TurnContext
from botbuilder.schema import Activity
from botframework.connector.auth import MicrosoftAppCredentials
import time  # Import the time module

class TeamsBotService:
    def __init__(self):
        self.config = TeamsConfig()
        self.adapter = BotFrameworkAdapter(
            app_id=self.config.BOT_ID, 
            app_password=self.config.BOT_PASSWORD
        )
        self._access_token = None
        self._token_expiry_time = 0
        
    async def process_activity(self, request_body, request_headers):
        """Process incoming Teams activity"""
        activity = Activity().deserialize(request_body)
        auth_header = request_headers.get("Authorization", "")
        
        async def callback(turn_context: TurnContext):
            await self._handle_turn(turn_context)
        
        await self.adapter.process_activity(activity, auth_header, callback)
        
    async def _handle_turn(self, turn_context: TurnContext):
        """Handle a turn of conversation"""
        text = turn_context.activity.text.lower() if turn_context.activity.text else ""
        if text.startswith('/storyteller') or 'write story' in text:
            prompt = text.replace('/storyteller', '').replace('write story', '').strip()
            await self._generate_story(turn_context, prompt)
        else:
            await turn_context.send_activity(
                "Please use the /storyteller command or type 'write story' followed by your prompt."
            )
    
    async def _generate_story(self, turn_context: TurnContext, prompt: str):
        """Generate a story using OpenAI"""
        try:
            # TODO: Implement OpenAI story generation
            story = f"Once upon a time... {prompt}"
            await turn_context.send_activity(story)
        except Exception as e:
            await turn_context.send_activity(
                "Sorry, I encountered an error generating your story. Please try again."
            )
    
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
        # Check if token exists and is not expired (with a 5-minute buffer)
        current_time = time.time()
        if self._access_token and self._token_expiry_time > (current_time + 300):
            print("[Teams Bot] Using cached access token.")
            return self._access_token
        
        print("[Teams Bot] Requesting new access token...")
        # This should be implemented with proper token caching and refresh
        # For now, using the client credentials flow
        token_url = f"https://login.microsoftonline.com/{self.config.TENANT_ID}/oauth2/v2.0/token"
        data = {
            'client_id': self.config.CLIENT_ID,
            'client_secret': self.config.CLIENT_SECRET,
            'scope': 'https://graph.microsoft.com/.default',
            'grant_type': 'client_credentials'
        }
        
        try:
            response = requests.post(token_url, data=data)
            response.raise_for_status()  # Raises HTTPError for bad responses (4XX, 5XX)
            token_data = response.json()
            
            self._access_token = token_data['access_token']
            # Calculate expiry time (current time + expires_in seconds)
            self._token_expiry_time = current_time + token_data.get('expires_in', 3600) 
            print("[Teams Bot] New access token obtained.")
            return self._access_token
        except requests.exceptions.RequestException as e:
            print(f"[Teams Bot] Error requesting access token: {e}")
            # Reset cache on error
            self._access_token = None
            self._token_expiry_time = 0
            raise  # Re-raise the exception so the caller knows about the failure
        except KeyError:
            print("[Teams Bot] Error: 'access_token' or 'expires_in' not found in token response.")
            self._access_token = None
            self._token_expiry_time = 0
            raise ValueError("Invalid token response received from Microsoft identity platform.")
    
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
