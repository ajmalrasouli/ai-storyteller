"""
Migration script to add audio_url column to Story table
"""
from sqlalchemy import Column, String, text
from extensions import db
from create_app import create_app  # Import create_app to get the Flask application context
from models.models import Story

def run_migration():
    print("Starting migration to add audio_url column to Story table...")
    app = create_app()
    with app.app_context():
        # Check if the column already exists
        inspector = db.inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('story')]
        
        if 'audio_url' not in columns:
            print("Adding audio_url column to Story table...")
            # Execute the raw SQL to add the column using current SQLAlchemy syntax
            with db.engine.connect() as conn:
                conn.execute(text('ALTER TABLE story ADD COLUMN audio_url VARCHAR(500)'))
                conn.commit()
            print("Migration successful!")
        else:
            print("audio_url column already exists in Story table, no changes made.")

if __name__ == "__main__":
    run_migration()
