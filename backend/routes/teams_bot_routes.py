from flask import Blueprint, request, jsonify
from ..services.teams_bot_service import TeamsBotService

bp = Blueprint('teams_bot', __name__, url_prefix='/teams/bot')
teams_bot_service = TeamsBotService()

@bp.route('/message', methods=['POST'])
def send_message():
    """Send a message to Teams"""
    data = request.json
    team_id = data.get('team_id')
    channel_id = data.get('channel_id')
    message = data.get('message')
    
    if not team_id or not channel_id or not message:
        return jsonify({'error': 'team_id, channel_id, and message are required'}), 400
    
    try:
        result = teams_bot_service.send_message(team_id, channel_id, message)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/card', methods=['POST'])
def send_card():
    """Send a card message to Teams"""
    data = request.json
    team_id = data.get('team_id')
    channel_id = data.get('channel_id')
    card_data = data.get('card')
    
    if not team_id or not channel_id or not card_data:
        return jsonify({'error': 'team_id, channel_id, and card are required'}), 400
    
    try:
        result = teams_bot_service.send_card_message(team_id, channel_id, card_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/activity', methods=['POST'])
def handle_activity():
    print("[Teams Bot] Received POST /teams/bot/activity")
    try:
        # Process the activity using the bot service (sync version)
        data = request.get_json()
        headers = request.headers
        # If your TeamsBotService.process_activity is async, you need to refactor it to sync or use asyncio.run
        # For now, just log and return a dummy response for connectivity test
        print(f"[Teams Bot] Headers: {headers}")
        print(f"[Teams Bot] Data: {data}")
        return jsonify({'status': 'success', 'message': 'Activity received'}), 200
    except Exception as e:
        print(f"[Teams Bot] Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
