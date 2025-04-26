from flask import Blueprint, request, send_file
from backend.services.azure_services import AzureServices
import io

bp = Blueprint('speech', __name__)
azure_services = AzureServices()

@bp.route('/api/speech', methods=['POST'])
def text_to_speech():
    data = request.json
    
    if not data or not data.get('text'):
        return {'error': 'Text is required'}, 400
    
    try:
        audio_data = azure_services.text_to_speech(data['text'])
        
        # Create a BytesIO object to send the audio data
        audio_stream = io.BytesIO(audio_data)
        audio_stream.seek(0)
        
        return send_file(
            audio_stream,
            mimetype='audio/wav',
            as_attachment=True,
            download_name='speech.wav'
        )
        
    except Exception as e:
        return {'error': str(e)}, 500 