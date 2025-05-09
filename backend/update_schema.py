from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Add backend directory to Python path
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models to ensure they're registered with SQLAlchemy
from backend.models.models import Story

if __name__ == '__main__':
    with app.app_context():
        # Drop all tables
        print("Dropping all tables...")
        db.drop_all()
        
        # Create all tables
        print("Creating all tables...")
        db.create_all()
        print("Database schema updated successfully!")
