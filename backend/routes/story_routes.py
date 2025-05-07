from flask import Blueprint, request, jsonify, current_app # Import current_app
from models.models import Story, User # Absolute import
from extensions import db # Absolute import
import json
import traceback
import sys
from flask_cors import CORS

bp = Blueprint('stories', __name__)
# CORS handled globally in create_app for /api/*, or keep specific here if needed
# CORS(bp, origins=["http://localhost:5173", "http://localhost:5174"])

def safe_json_loads(val):
    try:
        if not val or not isinstance(val, str) or val.strip() == '':
            return [] # Return empty list if val is None, empty string, or not a string
        return json.loads(val)
    except (json.JSONDecodeError, TypeError) as e:
         current_app.logger.error(f"Failed to decode JSON: '{val}'. Error: {e}")
         return [] # Return empty list on error

@bp.route('/stories', methods=['GET']) # OPTIONS handled by Flask-CORS globally
def get_stories():
    current_app.logger.info("GET /api/stories requested")
    try:
        stories = Story.query.order_by(Story.created_at.desc()).all()
        return jsonify([{
            'id': story.id,
            'title': story.title,
            'content': story.content,
            'theme': story.theme,
            'characters': safe_json_loads(story.characters),
            'ageGroup': story.age_group,
            'isFavorite': story.is_favorite,
            'imageUrl': story.image_url,
            'createdAt': story.created_at.isoformat() if story.created_at else None
        } for story in stories])
    except Exception as e:
        current_app.logger.error(f"Error fetching stories: {e}", exc_info=True)
        return jsonify({'error': 'Failed to retrieve stories'}), 500


@bp.route('/stories', methods=['POST']) # OPTIONS handled by Flask-CORS globally
def create_story():
    current_app.logger.info("POST /api/stories requested")
    data = request.json
    current_app.logger.debug(f"Incoming data: {data}")

    required_fields = ['theme', 'characters', 'age_group']
    if not data or not all(field in data and data[field] is not None for field in required_fields):
        missing = [field for field in required_fields if field not in data or data[field] is None]
        error_msg = f"Missing required fields: {', '.join(missing)}"
        current_app.logger.error(error_msg)
        return jsonify({'error': error_msg}), 400

    # Use current_app to access the initialized AzureServices instance
    azure_services = current_app.azure_services

    try:
        # Generate story content
        current_app.logger.info("Generating story content...")
        story_content = azure_services.generate_story(
            data['theme'],
            json.dumps(data['characters']), # Assuming characters is a list/dict
            data['age_group']
        )
        if not story_content or story_content.startswith("Error:"):
             current_app.logger.error(f"Story generation failed: {story_content}")
             return jsonify({'error': story_content or 'Story generation failed'}), 500
        current_app.logger.info("Story content generated.")

        # Extract/Generate title
        title = data.get('title', '').strip()
        if not title:
            try:
                # Attempt to extract from markdown style: **Title**
                if '**' in story_content and '**\n' in story_content:
                    title = story_content.split('**')[1].strip()
                else: # Fallback title generation
                    char_list = data.get('characters', [])
                    characters_str = ', '.join(char_list[:2]) if isinstance(char_list, list) and char_list else 'friends'
                    title = f"{data['theme'].capitalize()} Adventure with {characters_str}"
            except Exception as title_ex:
                 current_app.logger.warning(f"Could not auto-extract title: {title_ex}. Using generic title.")
                 title = f"{data['theme'].capitalize()} Story"

        current_app.logger.info(f"Using title: {title}")

        # Generate illustration
        current_app.logger.info("Generating illustration...")
        image_url = azure_services.generate_illustration(
            title,
            data['theme'],
            json.dumps(data['characters']),
            data['age_group']
        )
        if not image_url: # Check if illustration generation failed
             current_app.logger.warning("Illustration generation failed or returned None. Check Azure DALL-E logs/config.")
             # Decide whether to use a placeholder or return an error
             # For now, let's allow story creation without image
             image_url = None # Or a placeholder path like '/static/placeholder.png'

        # Create and save story
        story = Story(
            title=title,
            content=story_content,
            theme=data['theme'],
            characters=json.dumps(data['characters']), # Ensure characters are stored as JSON string
            age_group=data['age_group'],
            image_url=image_url,
            is_favorite=data.get('isFavorite', False) # Allow setting favorite on creation
        )
        db.session.add(story)
        db.session.commit()
        current_app.logger.info(f"Story created successfully with ID: {story.id}")

        return jsonify({
            'id': story.id,
            'title': story.title,
            'content': story.content,
            'theme': story.theme,
            'characters': safe_json_loads(story.characters),
            'ageGroup': story.age_group,
            'isFavorite': story.is_favorite,
            'imageUrl': story.image_url,
            'createdAt': story.created_at.isoformat() if story.created_at else None
        }), 201

    except Exception as e:
        db.session.rollback() # Rollback transaction on error
        current_app.logger.error(f"Exception in create_story: {e}", exc_info=True)
        return jsonify({'error': 'An internal server error occurred while creating the story.'}), 500


@bp.route('/stories/<int:story_id>/favorite', methods=['POST']) # OPTIONS handled by CORS
def toggle_favorite(story_id):
    current_app.logger.info(f"POST /api/stories/{story_id}/favorite")
    story = db.session.get(Story, story_id) # Use newer get() method
    if not story:
        return jsonify({'error': 'Story not found'}), 404

    try:
        story.is_favorite = not story.is_favorite
        db.session.commit()
        current_app.logger.info(f"Toggled favorite for story {story_id} to {story.is_favorite}")
        return jsonify({'isFavorite': story.is_favorite})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error toggling favorite for story {story_id}: {e}", exc_info=True)
        return jsonify({'error': 'Failed to update favorite status'}), 500

@bp.route('/stories/<int:story_id>', methods=['DELETE']) # OPTIONS handled by CORS
def delete_story(story_id):
    current_app.logger.info(f"DELETE /api/stories/{story_id}")
    story = db.session.get(Story, story_id)
    if not story:
        return jsonify({'error': 'Story not found'}), 404

    try:
        # Optional: Delete associated files from storage here if needed
        # e.g., if image_url points to Azure blob, delete the blob

        db.session.delete(story)
        db.session.commit()
        current_app.logger.info(f"Successfully deleted story {story_id}")
        return '', 204 # No content response for successful delete
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting story {story_id}: {e}", exc_info=True)
        return jsonify({'error': 'Failed to delete story'}), 500

@bp.route('/stories/<int:story_id>/regenerate-illustration', methods=['POST']) # OPTIONS handled by CORS
def regenerate_illustration(story_id):
    current_app.logger.info(f"POST /api/stories/{story_id}/regenerate-illustration")
    story = db.session.get(Story, story_id)
    if not story:
        return jsonify({'error': 'Story not found'}), 404

    azure_services = current_app.azure_services

    try:
        image_url = azure_services.generate_illustration(
            story.title,
            story.theme,
            story.characters, # Already a JSON string in DB
            story.age_group
        )
        if not image_url:
            return jsonify({'error': 'Illustration generation failed'}), 500

        story.image_url = image_url
        db.session.commit()
        current_app.logger.info(f"Illustration regenerated for story {story_id}")
        return jsonify({'imageUrl': image_url})

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error regenerating illustration for story {story_id}: {e}", exc_info=True)
        return jsonify({'error': 'Failed to regenerate illustration'}), 500