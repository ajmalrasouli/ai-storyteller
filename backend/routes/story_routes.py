# backend/routes/story_routes.py

from flask import Blueprint, request, jsonify, current_app
# --- Use ABSOLUTE IMPORTS relative to /app ---
from backend.models.models import Story, User
from backend.extensions import db
# ---------------------------
import json
import traceback
import sys
import uuid

bp = Blueprint('stories', __name__)
# CORS handled globally

def safe_json_loads(val):
    try:
        if not val or not isinstance(val, str) or val.strip() == '':
            return []
        return json.loads(val)
    except (json.JSONDecodeError, TypeError) as e:
         # Use current_app logger if available, otherwise print
         try:
            current_app.logger.error(f"Failed to decode JSON: '{val}'. Error: {e}")
         except RuntimeError: # Handle case where logger isn't setup yet (less likely here)
            print(f"ERROR: Failed to decode JSON: '{val}'. Error: {e}", file=sys.stderr)
         return []

@bp.route('/stories', methods=['GET'])
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
            'audioUrl': story.audio_url,
            'createdAt': story.created_at.isoformat() if story.created_at else None
        } for story in stories])
    except Exception as e:
        current_app.logger.error(f"Error fetching stories: {e}", exc_info=True)
        return jsonify({'error': 'Failed to retrieve stories'}), 500


@bp.route('/stories', methods=['POST'])
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

    azure_services = current_app.azure_services
    persistent_image_url = None

    try:
        # 1. Generate story content
        current_app.logger.info("Generating story content...")
        story_content = azure_services.generate_story(
            data['theme'],
            json.dumps(data['characters']),
            data['age_group']
        )
        if not story_content or story_content.startswith("Error:"):
             current_app.logger.error(f"Story generation failed: {story_content}")
             return jsonify({'error': story_content or 'Story generation failed'}), 500
        current_app.logger.info("Story content generated.")

        # 2. Extract/Generate title
        title = data.get('title', '').strip()
        if not title:
            try:
                if '**' in story_content and '**\n' in story_content:
                    title = story_content.split('**')[1].strip()
                else:
                    char_list = data.get('characters', [])
                    characters_str = ', '.join(char_list[:2]) if isinstance(char_list, list) and char_list else 'friends'
                    title = f"{data['theme'].capitalize()} Adventure with {characters_str}"
            except Exception as title_ex:
                 current_app.logger.warning(f"Could not auto-extract title: {title_ex}. Using generic title.")
                 title = f"{data['theme'].capitalize()} Story"
        current_app.logger.info(f"Using title: {title}")

        # 3. Generate illustration (gets temporary URL)
        current_app.logger.info("Generating illustration (temporary URL)...")
        temp_image_url = azure_services.generate_illustration(
            title,
            data['theme'],
            json.dumps(data['characters']),
            data['age_group']
        )

        # 4. Download image and upload to Blob Storage
        if temp_image_url:
            if azure_services.image_container_client:
                image_blob_name = f"illustrations/{uuid.uuid4()}.png"
                current_app.logger.info(f"Uploading illustration to blob: {image_blob_name}")
                persistent_image_url = azure_services.upload_blob_from_url(
                    container_client=azure_services.image_container_client,
                    blob_name=image_blob_name,
                    source_url=temp_image_url
                )
                if not persistent_image_url:
                    current_app.logger.error("Failed to upload illustration to blob storage.")
                    persistent_image_url = None
                else:
                    current_app.logger.info(f"Illustration uploaded to: {persistent_image_url}")
            else:
                current_app.logger.error("Image container client not available, cannot upload illustration.")
        else:
            current_app.logger.warning("Illustration generation failed or returned no URL.")

        # 5. Create and save story to DB
        story = Story(
            title=title,
            content=story_content,
            theme=data['theme'],
            characters=json.dumps(data['characters']),
            age_group=data['age_group'],
            image_url=persistent_image_url,
            is_favorite=data.get('isFavorite', False)
        )
        db.session.add(story)
        db.session.commit()
        current_app.logger.info(f"Story created successfully with ID: {story.id}")

        # 6. Return response
        return jsonify({
            'id': story.id,
            'title': story.title,
            'content': story.content,
            'theme': story.theme,
            'characters': safe_json_loads(story.characters),
            'ageGroup': story.age_group,
            'isFavorite': story.is_favorite,
            'imageUrl': story.image_url,
            'audioUrl': story.audio_url,
            'createdAt': story.created_at.isoformat() if story.created_at else None
        }), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Exception in create_story: {e}", exc_info=True)
        return jsonify({'error': 'An internal server error occurred while creating the story.'}), 500

@bp.route('/stories/<int:story_id>', methods=['DELETE'])
def delete_story(story_id):
    current_app.logger.info(f"DELETE /api/stories/{story_id}")
    story = db.session.get(Story, story_id)
    if not story:
        return jsonify({'error': 'Story not found'}), 404

    azure_services = current_app.azure_services
    image_blob_name = None
    audio_blob_name = None

    if story.image_url and azure_services.image_container_client:
        try:
            # Basic parsing assuming URL format like .../container_name/blob_name
            image_blob_name = story.image_url.split(f'{azure_services.image_container_client.container_name}/')[-1].split('?')[0] # Handle potential SAS tokens
        except Exception: pass
    if story.audio_url and azure_services.audio_container_client:
         try:
            audio_blob_name = story.audio_url.split(f'{azure_services.audio_container_client.container_name}/')[-1].split('?')[0]
         except Exception: pass

    try:
        db.session.delete(story)
        db.session.commit()
        current_app.logger.info(f"Successfully deleted story {story_id} from database.")

        # Attempt to delete blobs
        if image_blob_name and azure_services.image_container_client:
            try:
                current_app.logger.info(f"Attempting to delete image blob: {image_blob_name}")
                azure_services.image_container_client.delete_blob(image_blob_name)
                current_app.logger.info(f"Deleted image blob: {image_blob_name}")
            except Exception as blob_ex:
                current_app.logger.error(f"Failed to delete image blob {image_blob_name}: {blob_ex}")
        if audio_blob_name and azure_services.audio_container_client:
             try:
                current_app.logger.info(f"Attempting to delete audio blob: {audio_blob_name}")
                azure_services.audio_container_client.delete_blob(audio_blob_name)
                current_app.logger.info(f"Deleted audio blob: {audio_blob_name}")
             except Exception as blob_ex:
                 current_app.logger.error(f"Failed to delete audio blob {audio_blob_name}: {blob_ex}")

        return '', 204
    except Exception as e:
        current_app.logger.error(f"Error during story deletion process {story_id}: {e}", exc_info=True)
        return jsonify({'error': 'Failed to delete story resources'}), 500

@bp.route('/stories/<int:story_id>/favorite', methods=['POST'])
def toggle_favorite(story_id):
    current_app.logger.info(f"POST /api/stories/{story_id}/favorite")
    story = db.session.get(Story, story_id)
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

@bp.route('/stories/<int:story_id>/regenerate-illustration', methods=['POST'])
def regenerate_illustration(story_id):
    current_app.logger.info(f"POST /api/stories/{story_id}/regenerate-illustration")
    story = db.session.get(Story, story_id)
    if not story:
        return jsonify({'error': 'Story not found'}), 404

    azure_services = current_app.azure_services
    persistent_image_url = story.image_url # Default to old one

    try:
        temp_image_url = azure_services.generate_illustration(
            story.title,
            story.theme,
            story.characters,
            story.age_group
        )

        if temp_image_url:
            if azure_services.image_container_client:
                 old_image_blob_name = None
                 if story.image_url:
                     try: # Try to get old blob name to delete it
                         old_image_blob_name = story.image_url.split(f'{azure_services.image_container_client.container_name}/')[-1].split('?')[0]
                     except Exception: pass

                 image_blob_name = f"illustrations/{uuid.uuid4()}.png"
                 current_app.logger.info(f"Uploading regenerated illustration to blob: {image_blob_name}")
                 persistent_image_url = azure_services.upload_blob_from_url(
                    container_client=azure_services.image_container_client,
                    blob_name=image_blob_name,
                    source_url=temp_image_url
                 )
                 if persistent_image_url:
                      current_app.logger.info(f"Regenerated illustration uploaded to: {persistent_image_url}")
                      # Try deleting old blob after successful upload
                      if old_image_blob_name and old_image_blob_name != image_blob_name:
                          try:
                              azure_services.image_container_client.delete_blob(old_image_blob_name)
                              current_app.logger.info(f"Deleted old illustration blob: {old_image_blob_name}")
                          except Exception as del_ex:
                              current_app.logger.warning(f"Failed to delete old illustration blob {old_image_blob_name}: {del_ex}")
                 else:
                      current_app.logger.error("Failed to upload regenerated illustration.")
                      persistent_image_url = story.image_url # Revert to old one
            else:
                 current_app.logger.error("Image container client not available for regeneration.")
        else:
             current_app.logger.warning("Regeneration failed or returned no URL.")

        story.image_url = persistent_image_url
        db.session.commit()
        return jsonify({'imageUrl': story.image_url})

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error regenerating illustration for story {story_id}: {e}", exc_info=True)
        return jsonify({'error': 'Failed to regenerate illustration'}), 500