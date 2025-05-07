from flask import Blueprint, jsonify
import datetime # Absolute import (standard library)

bp = Blueprint('health', __name__, url_prefix='/health')

@bp.route('/', methods=['GET'])
def health_check():
    """Return health status of the application"""
    # Add more checks here if needed (e.g., database connection)
    return jsonify({
        'status': 'healthy',
        'message': 'Application is running',
        'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat() # Use timezone aware
    })

# Simple route for quick connectivity test
@bp.route('/ping', methods=['GET'])
def ping():
    return "pong", 200