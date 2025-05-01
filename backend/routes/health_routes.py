from flask import Blueprint, jsonify

bp = Blueprint('health', __name__, url_prefix='/health')

@bp.route('/', methods=['GET'])
def health_check():
    """Return health status of the application"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })
