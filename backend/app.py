import os
from dotenv import load_dotenv
from create_app import create_app
from flask_cors import CORS
from routes.health_routes import bp as health_bp

# Try to load environment variables from .env but continue if not found
try:
    load_dotenv()
    print("Attempted to load .env file")
except Exception as e:
    print(f"No .env file found or error loading it: {str(e)}")
    print("Will use system environment variables instead")

# Debug: Print environment variables
print("Environment Variables:")
print(f"AZURE_OPENAI_API_KEY: {'Set' if os.getenv('AZURE_OPENAI_API_KEY') else 'Not Set'}")
print(f"AZURE_OPENAI_ENDPOINT: {'Set' if os.getenv('AZURE_OPENAI_ENDPOINT') else 'Not Set'}")
print(f"AZURE_OPENAI_DEPLOYMENT_NAME: {'Set' if os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME') else 'Not Set'}")
print(f"AZURE_SPEECH_KEY: {'Set' if os.getenv('AZURE_SPEECH_KEY') else 'Not Set'}")
print(f"AZURE_SPEECH_REGION: {'Set' if os.getenv('AZURE_SPEECH_REGION') else 'Not Set'}")

app = create_app()

# Register blueprints
app.register_blueprint(health_bp)

# Configure CORS
CORS(app, origins=[
    "http://localhost:5174",  # Allow frontend dev server
    "https://ai-storyteller.render.com",  # Allow production URL
    "https://proud-water-076db370f.6.azurestaticapps.net", # Static web app
    "https://*.teams.microsoft.com",  # Teams domains
    "https://*.office.com",          # Office domains
    "https://*.office365.com"        # Office 365 domains
])

if __name__ == '__main__':
    app.run(debug=True)