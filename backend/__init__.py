from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from .config.config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configure app
    app.config.from_object(Config)
    
    # Initialize CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import and register blueprints
    from .routes import story_routes, auth_routes, speech_routes
    app.register_blueprint(story_routes.bp, url_prefix='/api')
    app.register_blueprint(auth_routes.bp, url_prefix='/api')
    app.register_blueprint(speech_routes.bp, url_prefix='/api')
    
    return app 