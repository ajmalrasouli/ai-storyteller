import os
import sys # Added for sys.stdout
import logging
from flask import Flask
from flask_cors import CORS
from flask_executor import Executor

# Use absolute imports from the 'backend' (app) root
from extensions import db, migrate
from services.azure_services import AzureServices # Corrected path based on class usage

# --- REMOVE TEAMS IMPORTS ---
# from routes import story_routes, auth_routes, speech_routes, teams_bot_routes, health_routes
# --- USE THIS INSTEAD ---
from routes import story_routes, auth_routes, speech_routes, health_routes # Removed teams_bot_routes

# Initialize extensions that don't need app context immediately
executor = Executor()

def create_app(config_object_path='config.config.Config'):
    """Flask application factory."""
    app = Flask(__name__)
    app.logger.info(f"Attempting to load config from: {config_object_path}")
    try:
        app.config.from_object(config_object_path)
        app.logger.info("Configuration loaded successfully.")
    except ImportError as e:
        app.logger.error(f"Failed to import configuration object at '{config_object_path}': {e}")
        app.logger.error("Ensure config/config.py exists and the Config class is defined.")
    except Exception as e:
         app.logger.error(f"An unexpected error occurred loading config: {e}", exc_info=True)

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
    app.azure_services = AzureServices(app.config)
    app.logger.info("AzureServices instance created and attached to app.")

    # Log status of critical clients from AzureServices
    app.logger.info(f"AzureServices: OpenAI Client ready: {bool(app.azure_services.text_client)}")
    app.logger.info(f"AzureServices: DALL-E Client ready: {bool(app.azure_services.dalle_client)}")
    app.logger.info(f"AzureServices: Speech Config ready: {bool(app.azure_services.speech_config)}")
    app.logger.info(f"AzureServices: Blob Client ready: {bool(app.azure_services.blob_container_client)}")
    app.logger.info(f"AzureServices: Share Client ready: {bool(app.azure_services.share_client)}")

    # --- Register blueprints ---
    app.register_blueprint(story_routes.bp, url_prefix='/api')
    app.register_blueprint(auth_routes.bp, url_prefix='/api')
    app.register_blueprint(speech_routes.bp, url_prefix='/api')
    app.register_blueprint(health_routes.bp)
    # --- REMOVED TEAMS BLUEPRINT REGISTRATION ---
    # app.register_blueprint(teams_bot_routes.bp)

    app.logger.info("Blueprints registered.")
    app.logger.info("Flask app creation completed.")
    return app