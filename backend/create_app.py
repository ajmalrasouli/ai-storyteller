# backend/create_app.py
import os
import sys
import logging
from flask import Flask
from flask_cors import CORS
from flask_executor import Executor

# --- Use RELATIVE IMPORTS relative to /app ---
from backend.extensions import db, migrate
from backend.config.config import Config
from backend.services.azure_services import AzureServices
from backend.routes import story_routes, auth_routes, speech_routes, health_routes
from backend.models.models import Story, User
from backend.config.config import Config
executor = Executor()

# Use the imported Config class as the default
def create_app(config_object=Config): # Pass the class directly
    """Flask application factory."""
    app = Flask(__name__)
    # Set database configuration before initializing extensions
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Use the config_object passed (defaults to the imported Config)
    app.logger.info(f"Attempting to load config from object: {config_object.__name__}")
    try:
        app.config.from_object(config_object) # Load config from the object
        app.logger.info("Configuration loaded successfully.")
    except Exception as e:
         app.logger.error(f"An unexpected error occurred loading config: {e}", exc_info=True)

    # Set port configuration
    app.config['PORT'] = os.getenv('FLASK_RUN_PORT', 5000)
    app.config['HOST'] = os.getenv('FLASK_RUN_HOST', '0.0.0.0')

    # --- Configure Logging ---
    log_level = logging.DEBUG if app.config.get('DEBUG') else logging.INFO
    app.logger.setLevel(log_level)
    if not app.logger.handlers:
        stream_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)
        app.logger.addHandler(stream_handler)
    app.logger.info(f"Flask logging configured at level: {logging.getLevelName(app.logger.level)}")

    # Initialize CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.logger.info("CORS initialized for /api/* routes.")

    # --- Initialize extensions ---
    db.init_app(app)
    migrate.init_app(app, db)
    executor.init_app(app)
    app.logger.info("Flask extensions (SQLAlchemy, Migrate, Executor) initialized.")

    # --- Initialize Azure Services and store instance on app ---
    app.logger.info("Initializing AzureServices...")
    # Pass the Flask app's config dictionary
    app.azure_services = AzureServices(app.config)
    app.logger.info("AzureServices instance created and attached to app.")

    # Log status of critical clients from AzureServices
    app.logger.info(f"AzureServices: OpenAI Client ready: {bool(app.azure_services.text_client)}")
    app.logger.info(f"AzureServices: DALL-E Client ready: {bool(app.azure_services.dalle_client)}")
    app.logger.info(f"AzureServices: Speech Config ready: {bool(app.azure_services.speech_config)}")
    app.logger.info(f"AzureServices: Image Container Client ready: {bool(app.azure_services.image_container_client)}")
    app.logger.info(f"AzureServices: Audio Container Client ready: {bool(app.azure_services.audio_container_client)}")
    app.logger.info(f"AzureServices: Share Client ready: {bool(app.azure_services.share_client)}")

    # --- Register blueprints ---
    app.register_blueprint(story_routes.bp, url_prefix='/api')
    app.register_blueprint(auth_routes.bp, url_prefix='/api')
    app.register_blueprint(speech_routes.bp, url_prefix='/api')
    app.register_blueprint(health_routes.bp)

    app.logger.info("Blueprints registered.")
    app.logger.info("Flask app creation completed.")
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=True)