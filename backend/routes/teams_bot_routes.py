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
async def handle_activity():
    """Handle incoming Teams activities"""
    try:
        # Process the activity using the bot service
        await teams_bot_service.process_activity(
            request.get_json(),
            request.headers
        )
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        if activity_type == 'message':
            # Handle incoming messages
            message = activity.get('text')
            user_id = activity.get('from', {}).get('id')
            
            # Process the message and send a response
            response = f"Received your message: {message}"
            
            # Send response back to the user
            teams_bot_service.send_message(
                activity.get('team', {}).get('id'),
                activity.get('conversation', {}).get('id'),
                response
            )
            
            return jsonify({'status': 'success'})
        
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
