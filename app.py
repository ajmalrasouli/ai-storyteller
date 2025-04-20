from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from openai import AzureOpenAI
import os
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///stories.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)

# Configure Azure OpenAI with the working configuration from Azurekeycheck.py
endpoint = "https://ajmal-m9psmmwe-eastus2.openai.azure.com/"
AZURE_DEPLOYMENT = "gpt-4.1-mini"
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version=api_version,
    azure_endpoint=endpoint
)

# Debug route to check Azure OpenAI configuration
@app.route('/debug/config', methods=['GET'])
def debug_config():
    # Mask API key for security
    api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
    masked_key = api_key[:5] + "..." + api_key[-5:] if len(api_key) > 10 else "Not set"
    
    # Get configuration
    config = {
        "azure_openai_endpoint": endpoint,
        "azure_openai_api_key": masked_key,
        "azure_deployment_being_used": AZURE_DEPLOYMENT,
        "api_version": api_version
    }
    
    # Try to list deployments (will show if API key and endpoint are valid)
    deployment_info = "Could not check deployments - API key or endpoint may be invalid"
    try:
        # List available models in a safe way that doesn't crash if config is wrong
        from openai import AzureOpenAI
        test_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=api_version,
            azure_endpoint=endpoint
        )
        
        try:
            # This will either work or throw an exception
            models = test_client.models.list()
            deployment_info = "Available deployments: " + ", ".join([model.id for model in models.data])
        except Exception as e:
            deployment_info = f"Error listing deployments: {str(e)}"
    except Exception as e:
        deployment_info = f"Error initializing client: {str(e)}"
    
    config["deployment_status"] = deployment_info
    
    return jsonify(config)

# Enhanced fallback story generator
def generate_creative_story(theme, characters, age_group):
    # Story elements by theme
    theme_elements = {
        "Friendship": {
            "settings": ["a colorful playground", "a magical treehouse", "a summer camp", "a bustling school"],
            "challenges": ["a misunderstanding between friends", "helping a new student fit in", "working together on a difficult project", "standing up for each other"],
            "lessons": ["true friendship means accepting differences", "friends support each other through difficult times", "communication solves most problems", "the value of loyalty"]
        },
        "Adventure": {
            "settings": ["a mysterious island", "an enchanted forest", "outer space", "an underwater kingdom"],
            "challenges": ["finding a hidden treasure", "rescuing a magical creature", "solving an ancient puzzle", "crossing a dangerous canyon"],
            "lessons": ["courage in the face of fear", "the joy of discovery", "preparation is important", "teamwork makes difficult tasks possible"]
        },
        "Animals": {
            "settings": ["a busy animal hospital", "a vast wildlife sanctuary", "a colorful coral reef", "a dense jungle"],
            "challenges": ["helping a lost baby animal", "protecting an endangered species", "understanding animal language", "building a shelter for creatures"],
            "lessons": ["respecting all living beings", "the importance of habitat conservation", "animals have feelings too", "the balance of nature is delicate"]
        },
        "Magic": {
            "settings": ["a wizard's academy", "a kingdom of fairies", "a shop of magical objects", "a village where everything is enchanted"],
            "challenges": ["mastering a difficult spell", "stopping a mischievous magical prank", "finding a lost magical artifact", "breaking a troublesome curse"],
            "lessons": ["with great power comes responsibility", "magic is within everyone", "patience leads to mastery", "knowledge is its own form of magic"]
        },
        "Space": {
            "settings": ["a space station", "a distant planet", "an asteroid field", "a rocket ship"],
            "challenges": ["first contact with aliens", "navigating through a meteor shower", "repairing a damaged spacecraft", "terraforming a new world"],
            "lessons": ["the universe is vast and wonderful", "scientific discovery requires persistence", "home is where your heart is", "diversity makes us stronger"]
        }
    }
    
    # Default elements if theme not found
    default_elements = {
        "settings": ["a charming little town", "a secret garden", "a cozy cottage", "a busy city"],
        "challenges": ["solving a mystery", "overcoming a fear", "learning a new skill", "making new friends"],
        "lessons": ["believing in yourself", "never giving up", "helping others", "the importance of kindness"]
    }
    
    # Get story elements based on theme
    elements = theme_elements.get(theme, default_elements)
    
    # Select random elements
    setting = random.choice(elements["settings"])
    challenge = random.choice(elements["challenges"])
    lesson = random.choice(elements["lessons"])
    
    # Age-appropriate story structure
    if "0-4" in age_group:
        title = f"The {theme} Adventure"
        story = f"""Title: {title}

Once upon a time in {setting}, there lived {characters[0]}{' and ' + characters[1] if len(characters) > 1 else ''}.

Every day, they would play together and laugh. They loved to explore and have fun.

One day, they faced {challenge}. It was not easy! {characters[0]} felt a little scared.

{characters[1] if len(characters) > 1 else 'A helpful friend'} said, "Don't worry! We can do this together."

They worked hard and helped each other. Soon, the problem was solved!

They learned that {lesson}.

The End"""
    
    elif "5-8" in age_group:
        title = f"{characters[0]}'s {theme} Journey"
        story = f"""Title: {title}

In {setting}, there lived {", ".join(characters[:-1])}{' and ' + characters[-1] if len(characters) > 1 else characters[0]}.

They were the best of friends who loved to explore and discover new things together. Each of them had special talents: {characters[0]} was brave, {characters[1] if len(characters) > 1 else 'their friend'} was clever.

One beautiful morning, they discovered {challenge}. "This is going to be tricky," said {characters[0]}.

"Let's make a plan," suggested {characters[1] if len(characters) > 1 else 'their friend'}. They gathered their supplies and courage.

First, they tried to {random.choice(['climb the tallest tree for a better view', 'ask the wise old owl for advice', 'draw a map of the area', 'build a special tool to help them'])}.

When that didn't completely work, they {random.choice(['tried a different approach', 'asked for help from others', 'combined their ideas', 'remembered an important clue'])}.

After much effort and teamwork, they finally succeeded! Everyone celebrated their achievement.

From this adventure, they learned that {lesson}.

The End"""
    
    else:  # 9-12
        title = f"The Mystery of {theme}"
        story = f"""Title: {title}

Deep within {setting}, a group of friends faced an extraordinary challenge. {", ".join(characters[:-1])}{' and ' + characters[-1] if len(characters) > 1 else characters[0]} were known throughout their community for their curiosity and problem-solving abilities.

{characters[0]} was the leader, always ready with a plan. {characters[1] if len(characters) > 1 else 'Their companion'} was the thinker, analyzing every situation carefully. {characters[2] if len(characters) > 2 else 'Another friend'} brought creativity and unexpected ideas to the group.

Their adventure began when they discovered {challenge}. This wasn't like anything they had faced before.

"We need to approach this systematically," said {characters[0]}, outlining their first steps.

They researched ancient books, interviewed local experts, and gathered special equipment. Each step brought new revelations and sometimes new obstacles.

The most difficult moment came when {random.choice(['a sudden storm threatened their progress', 'an unexpected competitor tried to beat them to the solution', 'they realized they had been following the wrong clues', 'one of their tools broke at a critical moment'])}.

It was {characters[1] if len(characters) > 1 else characters[0]} who finally had the breakthrough insight: {random.choice(['patterns that seemed random actually followed a secret code', 'the solution was hidden in plain sight all along', 'by combining their different perspectives, the answer became clear', 'sometimes the simplest approach works best'])}.

With renewed determination, they completed their mission. Not only did they succeed, but they also helped their entire community in the process.

Through this experience, they truly understood that {lesson}. It was a lesson they would carry with them through all their future adventures.

The End"""
    
    return title, story

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    stories = db.relationship('Story', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    theme = db.Column(db.String(50), nullable=False)
    characters = db.Column(db.String(500), nullable=False)  # Store as JSON string
    age_group = db.Column(db.String(20), nullable=False)
    is_favorite = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create tables
with app.app_context():
    db.drop_all()  # Drop existing tables
    db.create_all()  # Create new tables

# Story routes
@app.route('/stories', methods=['GET'])
def get_stories():
    try:
        stories = Story.query.order_by(Story.created_at.desc()).all()
        return jsonify([{
            'id': story.id,
            'title': story.title,
            'content': story.content,
            'theme': story.theme,
            'characters': story.characters.split(','),
            'ageGroup': story.age_group,
            'isFavorite': story.is_favorite,
            'createdAt': story.created_at.isoformat()
        } for story in stories])
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/stories', methods=['POST'])
def create_story():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        if 'theme' not in data:
            return jsonify({'message': 'Missing required field: theme'}), 400

        if 'characters' not in data or not isinstance(data['characters'], list):
            return jsonify({'message': 'Missing or invalid characters field'}), 400

        if 'ageGroup' not in data:
            return jsonify({'message': 'Missing required field: ageGroup'}), 400
        
        # Generate story using Azure OpenAI
        prompt = f"""Create a children's story with the following details:
        Theme: {data['theme']}
        Characters: {', '.join(data['characters'])}
        Age Group: {data['ageGroup']} years old
        
        Please include:
        - A clear title
        - Age-appropriate vocabulary and concepts
        - An engaging plot with beginning, middle, and end
        - A moral or lesson related to the theme
        - Dialogue between characters
        - Descriptive language to paint a vivid picture
        
        Make it engaging, educational, and age-appropriate."""

        try:
            response = client.chat.completions.create(
                model=AZURE_DEPLOYMENT,
                messages=[
                    {"role": "system", "content": "You are a creative children's story writer with expertise in creating engaging, age-appropriate stories that entertain and teach valuable lessons."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            story_content = response.choices[0].message.content
            title = story_content.split('\n')[0].replace('Title:', '').strip()
            
        except Exception as api_error:
            print(f"Azure OpenAI API error: {str(api_error)}")
            # Fallback to enhanced local story generation if Azure API fails
            title, story_content = generate_creative_story(
                data['theme'],
                data['characters'],
                data['ageGroup']
            )

        # Create new story
        story = Story(
            title=title,
            content=story_content,
            theme=data['theme'],
            characters=','.join(data['characters']),
            age_group=data['ageGroup'],
            user_id=1  # Using a default user ID for now
        )
        db.session.add(story)
        db.session.commit()

        return jsonify({
            'id': story.id,
            'title': story.title,
            'content': story.content,
            'theme': story.theme,
            'characters': story.characters.split(','),
            'ageGroup': story.age_group,
            'isFavorite': story.is_favorite,
            'createdAt': story.created_at.isoformat()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@app.route('/stories/<int:story_id>/favorite', methods=['POST'])
def toggle_favorite(story_id):
    try:
        story = Story.query.get(story_id)
        if not story:
            return jsonify({'message': 'Story not found'}), 404

        story.is_favorite = not story.is_favorite
        db.session.commit()

        return jsonify({
            'id': story.id,
            'isFavorite': story.is_favorite
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 