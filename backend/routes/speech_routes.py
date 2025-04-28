from flask import Blueprint, request, send_file
from services.azure_services import AzureServices
from flask_cors import CORS
import io

bp = Blueprint('speech', __name__)
# Enable CORS for the speech blueprint
CORS(bp, origins=["http://localhost:5173", "http://localhost:5174"])
azure_services = AzureServices()

@bp.route('/speech', methods=['POST', 'OPTIONS'])
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
        
        # Create a BytesIO object to send the audio data
        audio_stream = io.BytesIO(audio_data)
        audio_stream.seek(0)
        
        print("[Speech API] Successfully generated speech, sending response")
        return send_file(
            audio_stream,
            mimetype='audio/wav',
            as_attachment=True,
            download_name='speech.wav'
        )
        
    except Exception as e:
        print(f"[Speech API] Error: {str(e)}")
        return {'error': str(e)}, 500