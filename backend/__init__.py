from flask import Flask
from flask_cors import CORS
from config.config import Config

# Import and register blueprints
from routes import story_routes, auth_routes, speech_routes