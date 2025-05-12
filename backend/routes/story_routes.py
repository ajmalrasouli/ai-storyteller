from flask import Blueprint, request, jsonify
from models.models import Story, User
from services.azure_services import AzureServices
from extensions import db
import json
import traceback as tb
from flask_cors import CORS, cross_origin

bp = Blueprint('stories', __name__)
CORS(bp, origins=["http://localhost:5173", "http://localhost:5174"])  # Enable CORS for frontend
azure_services = AzureServices()

def safe_json_loads(val):
    import json
    try:
        if not val or val.strip() == '':
            return []
        return json.loads(val)
    except Exception:
        return []

@bp.route('/stories', methods=['GET', 'OPTIONS'])
@cross_origin(origins=['https://proud-water-076db370f.6.azurestaticapps.net'], methods=['GET', 'OPTIONS'])
def get_stories():
    stories = Story.query.all()
    return jsonify([{  
        'id': story.id,
        'title': story.title,
        'content': story.content,
        'theme': story.theme,
        'characters': safe_json_loads(story.characters),
        'ageGroup': story.age_group,
        'isFavorite': story.is_favorite,
        'imageUrl': story.image_url,
        'audioUrl': getattr(story, 'audio_url', None),
        'createdAt': story.created_at.isoformat()
    } for story in stories])

@bp.route('/stories', methods=['POST', 'OPTIONS'])
@cross_origin(origins=['https://proud-water-076db370f.6.azurestaticapps.net'], methods=['POST', 'OPTIONS'])
def create_story():
    import sys
    import logging
    import traceback as tb
    data = request.json
    required_fields = ['theme', 'characters', 'age_group']  # Removed 'title' as it will be auto-generated
    # Log incoming request data
    print("[DEBUG] Incoming POST /stories data:", data, file=sys.stderr)
    if not all(field in data for field in required_fields):
        print("[ERROR] Missing required fields in request data", file=sys.stderr)
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        # Generate story content
        story_content = azure_services.generate_story(
            data['theme'],
            json.dumps(data['characters']),
            data['age_group']
        )
        
        # Extract title from the first line of the story content
        title = data.get('title', '')
        if not title:
            # If no title provided, extract from first line or generate based on theme
            if '**' in story_content and '**\n' in story_content:
                # Extract title from markdown format if present
                title = story_content.split('**')[1].strip()
            else:
                # Generate a simple title based on theme and characters
                characters_str = ', '.join(data['characters'][:2]) if data['characters'] else ''
                title = f"{data['theme']} Adventure with {characters_str}"
        
        print(f"[DEBUG] Using title: {title}", file=sys.stderr)
        
        # Save story content to storage
        try:
            story_url = azure_services.save_story_content(story_content, title)
            print(f"[DEBUG] Story content saved to: {story_url}", file=sys.stderr)
        except Exception as e:
            print(f"[ERROR] Failed to save story content: {str(e)}", file=sys.stderr)
            tb.print_exc(file=sys.stderr)
            story_url = None
        
        # Generate illustration and save to storage
        print(f"[DEBUG] Generating illustration for title: {title}", file=sys.stderr)
        try:
            image_data = azure_services.generate_illustration(
                title,
                data['theme'],
                json.dumps(data['characters']),
                data['age_group']
            )
            image_url = azure_services.save_image(image_data, title)
            print(f"[DEBUG] Successfully saved illustration: {image_url}", file=sys.stderr)
        except Exception as illustration_error:
            print(f"[ERROR] Failed to save illustration: {str(illustration_error)}", file=sys.stderr)
            tb.print_exc(file=sys.stderr)
            # Use a placeholder image instead of failing the whole request
            image_url = "/static/placeholder.png"
        
        # Generate and save audio to blob storage
        print(f"[DEBUG] Generating and saving audio for title: {title}", file=sys.stderr)
        try:
            audio_data = azure_services.text_to_speech(story_content)
            audio_url = azure_services.save_audio(audio_data, title)
            print(f"[DEBUG] Successfully saved audio: {audio_url}", file=sys.stderr)
        except Exception as audio_error:
            print(f"[ERROR] Failed to save audio: {str(audio_error)}", file=sys.stderr)
            tb.print_exc(file=sys.stderr)
            audio_url = None
        
        # Create story - handle case where audio_url column might not exist yet
        try:
            # First try creating with audio_url
            story = Story(
                title=title,
                content=story_content,
                theme=data['theme'],
                characters=json.dumps(data['characters']),
                age_group=data['age_group'],
                image_url=image_url,
                audio_url=audio_url
            )
        except TypeError as e:
            # If 'audio_url' is an invalid keyword argument, create without it
            if "'audio_url' is an invalid keyword argument" in str(e):
                print(f"[WARNING] Story model doesn't have audio_url column yet, creating without it", file=sys.stderr)
                story = Story(
                    title=title,
                    content=story_content,
                    theme=data['theme'],
                    characters=json.dumps(data['characters']),
                    age_group=data['age_group'],
                    image_url=image_url
                )
            else:
                raise
        db.session.add(story)
        db.session.commit()
        # Build response JSON, conditionally adding audioUrl if available
        response_data = {
            'id': story.id,
            'title': story.title,
            'content': story.content,
            'theme': story.theme,
            'characters': safe_json_loads(story.characters),
            'ageGroup': story.age_group,
            'imageUrl': story.image_url,
            'createdAt': story.created_at.isoformat()
        }
        
        # Only add audioUrl if it exists in the story model
        if hasattr(story, 'audio_url'):
            response_data['audioUrl'] = story.audio_url
        elif audio_url:  # If we have audio_url from generation but couldn't store it in the model
            response_data['audioUrl'] = audio_url
            
        return jsonify(response_data), 201
    except Exception as e:
        print("[ERROR] Exception in create_story:", str(e), file=sys.stderr)
        tb.print_exc(file=sys.stderr)
        # Return error and stack trace in response for easier debugging (remove in production)
        return jsonify({'error': str(e), 'traceback': tb.format_exc()}), 500

@bp.route('/stories/<int:story_id>/favorite', methods=['POST', 'OPTIONS'])
@cross_origin(origins=['https://proud-water-076db370f.6.azurestaticapps.net'], methods=['POST', 'OPTIONS'])
def toggle_favorite(story_id):
    if request.method == 'OPTIONS':
        return {'success': True}, 200
    
    story = Story.query.get_or_404(story_id)
    story.is_favorite = not story.is_favorite
    db.session.commit()
    return jsonify({'isFavorite': story.is_favorite})

@bp.route('/stories/<int:story_id>', methods=['DELETE', 'OPTIONS'])
@cross_origin(origins=['https://proud-water-076db370f.6.azurestaticapps.net'], methods=['DELETE', 'OPTIONS'])
def delete_story(story_id):
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        return {'success': True}, 200
    
    import sys
    print(f"[DEBUG] Attempting to delete story with ID: {story_id}", file=sys.stderr)
    
    try:
        story = Story.query.get(story_id)
        if not story:
            print(f"[ERROR] Story with ID {story_id} not found", file=sys.stderr)
            return jsonify({'error': f'Story with ID {story_id} not found'}), 404
        
        db.session.delete(story)
        db.session.commit()
        print(f"[DEBUG] Successfully deleted story with ID: {story_id}", file=sys.stderr)
        return '', 204
    except Exception as e:
        print(f"[ERROR] Failed to delete story with ID {story_id}: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@bp.route('/stories/<int:story_id>/regenerate-illustration', methods=['POST', 'OPTIONS'])
@cross_origin(origins=['https://proud-water-076db370f.6.azurestaticapps.net'], methods=['POST', 'OPTIONS'])
def regenerate_illustration(story_id):
    if request.method == 'OPTIONS':
        return {'success': True}, 200
    
    story = Story.query.get_or_404(story_id)
    
    try:
        image_url = azure_services.generate_illustration(
            story.title,
            story.theme,
            story.characters,
            story.age_group
        )
        
        story.image_url = image_url
        db.session.commit()
        
        return jsonify({'imageUrl': image_url})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 