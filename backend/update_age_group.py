from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import models to ensure they're registered with SQLAlchemy
from models.models import Story

if __name__ == '__main__':
    with app.app_context():
        # Create a connection
        conn = db.engine.connect()
        
        # Update the age_group column length
        conn.execute("ALTER TABLE story ALTER COLUMN age_group TYPE VARCHAR(100)")
        
        # Commit changes
        conn.commit()
        
        print("Successfully updated age_group column length to 100 characters")
