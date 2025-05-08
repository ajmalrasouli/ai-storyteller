from flask import Blueprint, request, send_file, current_app, make_response # Import current_app, make_response
from flask_cors import CORS
import io
from backend.services.azure_services import AzureServices

bp = Blueprint('speech', __name__)
# CORS handled globally in create_app for /api/*, or keep specific here if needed
# CORS(bp, origins=["http://localhost:5173", "http://localhost:5174"])

@bp.route('/speech', methods=['POST']) # OPTIONS handled by Flask-CORS globally
def text_to_speech():
    current_app.logger.info("POST /api/speech")
    data = request.json
    current_app.logger.debug(f"Incoming data: {data}")

    if not data or not data.get('text'):
        current_app.logger.error("Text field is missing from request")
        return jsonify({'error': 'Text is required'}), 400

    text_to_convert = data['text']
    azure_services = current_app.azure_services # Access via current_app

    try:
        current_app.logger.info(f"Converting text to speech (length: {len(text_to_convert)})...")
        audio_data = azure_services.text_to_speech(text_to_convert)

        if audio_data is None:
             current_app.logger.error("Text-to-speech conversion failed (returned None)")
             return jsonify({'error': 'Speech synthesis failed'}), 500

        audio_stream = io.BytesIO(audio_data)
        # Don't need seek(0) for send_file with BytesIO

        current_app.logger.info("Speech generated successfully, sending audio file.")
        # Use make_response for better header control if needed, or send_file directly
        response = make_response(send_file(
            audio_stream,
            mimetype='audio/mpeg', # Use mpeg for mp3 format set in AzureServices
            as_attachment=False, # Set to True if you want download prompt
            download_name='speech.mp3' # Use .mp3 extension
        ))
        # Add cache control headers to prevent caching if desired
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    except Exception as e:
        current_app.logger.error(f"Error during text-to-speech: {e}", exc_info=True)
        return jsonify({'error': 'An internal server error occurred during speech synthesis.'}), 500