from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Minimal app is running'
    })

@app.route('/teams/bot/activity', methods=['POST'])
def teams_bot():
    """Handle Teams bot activity"""
    try:
        data = request.json
        print(f'FULL TEAMS REQUEST: Headers: {request.headers}')
        print(f'FULL TEAMS PAYLOAD: {data}')
        
        # Process any command text from the message
        if data.get('type') == 'message':
            text = data.get('text', '').strip()
            if 'storyteller' in text:
                return jsonify({
                    "type": "message",
                    "text": "Hello! I'm AI Storyteller bot. I received your command!"
                })
        
        # Default response
        return jsonify({
            "type": "message", 
            "text": "I received your message!"
        })
    except Exception as e:
        print(f'Error processing Teams bot activity: {str(e)}')
        return jsonify({
            "type": "message",
            "text": f"Error: {str(e)}"
        })

# Print environment info for debugging
print("Starting minimal app...")
print(f"Running on port: 5000")
print(f"Environment variables:")
print(f"BOT_ID: {'Set' if os.getenv('BOT_ID') else 'Not Set'}")
print(f"BOT_PASSWORD: {'Set' if os.getenv('BOT_PASSWORD') else 'Not Set'}")

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 