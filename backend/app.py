import os
from dotenv import load_dotenv
from create_app import create_app
from flask_cors import CORS  # pip install flask-cors

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
if os.getenv('FLASK_ENV') == 'production':
    CORS(app, origins=["https://proud-water-076db370f.6.azurestaticapps.net", "http://localhost:5174"], supports_credentials=True)
else:
    CORS(app, origins=["http://localhost:5174", "http://localhost:5173"], supports_credentials=True)

if __name__ == '__main__':
    app.run(debug=True)