import os
from app import app

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')

if __name__ == '__main__':
    app.run()