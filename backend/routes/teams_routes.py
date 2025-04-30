from flask import Blueprint, request, redirect, url_for, jsonify
from ..services.teams_service import TeamsService
from ..config.teams_config import TeamsConfig

bp = Blueprint('teams', __name__, url_prefix='/teams')
teams_service = TeamsService()

@bp.route('/auth')
def auth():
    """Redirect to Teams authentication"""
    auth_url = teams_service.get_auth_url()
    return redirect(auth_url)

@bp.route('/callback')
def callback():
    """Handle Teams authentication callback"""
    auth_code = request.args.get('code')
    if not auth_code:
        return jsonify({'error': 'No authorization code provided'}), 400
    
    try:
        token_response = teams_service.get_access_token(auth_code)
        # Store token in session or database
        return redirect(url_for('index'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/send-message', methods=['POST'])
def send_message():
    """Send message to Teams"""
    data = request.json
    team_id = data.get('team_id')
    message = data.get('message')
    
    if not team_id or not message:
        return jsonify({'error': 'team_id and message are required'}), 400
    
    try:
        result = teams_service.send_message_to_team(team_id, message)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
