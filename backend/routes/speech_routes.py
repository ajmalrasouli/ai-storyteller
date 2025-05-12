from flask import Blueprint, request, send_file
from services.azure_services import AzureServices
from flask_cors import CORS, cross_origin
import io

bp = Blueprint('speech', __name__)
# Enable CORS for the speech blueprint
CORS(bp, origins=["http://localhost:5173", "http://localhost:5174", "https://proud-water-076db370f.6.azurestaticapps.net"])
azure_services = AzureServices()

@bp.route('/speech', methods=['POST', 'OPTIONS'])
@cross_origin(origins=['http://localhost:5173', 'http://localhost:5174', 'https://proud-water-076db370f.6.azurestaticapps.net'], methods=['POST', 'OPTIONS'])
def text_to_speech():
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        return {'success': True}, 200
        
    data = request.json
    print(f"[Speech API] Received request with data: {data}")
    
    if not data or not data.get('text'):
        print("[Speech API] Error: Text is required")
        return {'error': 'Text is required'}, 400
    
    try:
        print(f"[Speech API] Converting text to speech, length: {len(data['text'])}")
        audio_data = azure_services.text_to_speech(data['text'])
        # Save audio to Azure Blob Storage
        title = data.get('title', 'story_audio')
        audio_url = azure_services.save_audio(audio_data, title)
        print(f"[Speech API] Successfully generated and saved speech. audioUrl: {audio_url}")
        return {'audioUrl': audio_url}, 200
        
    except Exception as e:
        print(f"[Speech API] Error: {str(e)}")
        return {'error': str(e)}, 500