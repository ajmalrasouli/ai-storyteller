import os
from dotenv import load_dotenv
from create_app import create_app
from flask_cors import CORS
from routes.health_routes import bp as health_bp

# Load environment variables
load_dotenv()

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
    "https://ai-storyteller.render.com"  # Allow production URL
])

if __name__ == '__main__':
    app.run(debug=True)