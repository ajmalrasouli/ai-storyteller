from flask import Blueprint, request, jsonify
from backend.models.models import Story, User
from backend.services.azure_services import AzureServices
from backend import db
import json
import traceback

bp = Blueprint('stories', __name__)
azure_services = AzureServices()

@bp.route('/stories', methods=['GET'])
def get_stories():
    user_id = request.args.get('user_id')
    if user_id:
        stories = Story.query.filter_by(user_id=user_id).all()
    else:
        stories = Story.query.all()
    return jsonify([{
        'id': story.id,
        'title': story.title,
        'content': story.content,
        'theme': story.theme,
        'characters': json.loads(story.characters),
        'age_group': story.age_group,
        'is_favorite': story.is_favorite,
        'image_url': story.image_url,
        'created_at': story.created_at.isoformat()
    } for story in stories])

@bp.route('/stories', methods=['POST'])
def create_story():
    data = request.json
    required_fields = ['title', 'theme', 'characters', 'age_group']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        # Generate story content
        story_content = azure_services.generate_story(
            data['theme'],
            json.dumps(data['characters']),
            data['age_group']
        )
        # Generate illustration
        image_url = azure_services.generate_illustration(
            data['title'],
            data['theme'],
            json.dumps(data['characters']),
            data['age_group']
        )
        # Create story
        story = Story(
            title=data['title'],
            content=story_content,
            theme=data['theme'],
            characters=json.dumps(data['characters']),
            age_group=data['age_group'],
            image_url=image_url,
            user_id=data.get('user_id')
        )
        db.session.add(story)
        db.session.commit()
        return jsonify({
            'id': story.id,
            'title': story.title,
            'content': story.content,
            'theme': story.theme,
            'characters': json.loads(story.characters),
            'age_group': story.age_group,
            'image_url': story.image_url,
            'created_at': story.created_at.isoformat()
        }), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@bp.route('/stories/<int:story_id>/favorite', methods=['POST'])
def toggle_favorite(story_id):
    story = Story.query.get_or_404(story_id)
    story.is_favorite = not story.is_favorite
    db.session.commit()
    return jsonify({'is_favorite': story.is_favorite})

@bp.route('/stories/<int:story_id>', methods=['DELETE'])
def delete_story(story_id):
    story = Story.query.get_or_404(story_id)
    db.session.delete(story)
    db.session.commit()
    return '', 204

@bp.route('/stories/<int:story_id>/regenerate-illustration', methods=['POST'])
def regenerate_illustration(story_id):
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
        
        return jsonify({'image_url': image_url})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 