import sys
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from backend.create_app import create_app

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Load environment variables
load_dotenv()

# Create app
app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        print("Creating all tables...")
        db.create_all()
        print("Tables created successfully!")
