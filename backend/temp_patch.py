"""
Temporary patch to handle Story model without audio_url column
This can be added to story_routes.py to prevent errors until the database is migrated
"""

def create_story_with_audio_url_check(story_data):
    """
    Create a Story object with or without audio_url based on schema
    """
    from models.models import Story
    from sqlalchemy import inspect
    from extensions import db
    
    # Check if the column already exists in the database
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('story')]
    
    if 'audio_url' in columns:
        # If the column exists, include audio_url
        return Story(**story_data)
    else:
        # If the column doesn't exist, exclude audio_url
        if 'audio_url' in story_data:
            # Create a copy of the data without audio_url
            data_without_audio = story_data.copy()
            data_without_audio.pop('audio_url')
            return Story(**data_without_audio)
        else:
            return Story(**story_data)
