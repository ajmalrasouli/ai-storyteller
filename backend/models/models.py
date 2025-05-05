from datetime import datetime
from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    theme = db.Column(db.String(50), nullable=False)
    characters = db.Column(db.String(500), nullable=False)  # Store as JSON string
    age_group = db.Column(db.String(20), nullable=False)
    is_favorite = db.Column(db.Boolean, default=False)
    image_url = db.Column(db.String(500), nullable=True)  # URL for the AI-generated illustration
    created_at = db.Column(db.DateTime, default=datetime.utcnow)