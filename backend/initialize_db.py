import os
import sys
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import app, db, migrate

# Load environment variables
load_dotenv()

if __name__ == '__main__':
    with app.app_context():
        print("Initializing database...")
        db.create_all()
        print("Database tables created successfully!")
