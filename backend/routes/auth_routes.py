# backend/routes/auth_routes.py

from flask import Blueprint, request, jsonify, current_app
# --- CHANGE TO RELATIVE IMPORTS ---
# from models.models import User
from ..models.models import User
# from extensions import db
from ..extensions import db
# ----------------------------------
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    current_app.logger.info("POST /api/register")

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400

    try:
        user = User(email=data['email'])
        user.set_password(data['password']) # Uses generate_password_hash internally

        db.session.add(user)
        db.session.commit()
        current_app.logger.info(f"User {data['email']} registered successfully.")
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error registering user {data.get('email')}: {e}", exc_info=True)
        return jsonify({'error': 'Failed to register user'}), 500


@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    current_app.logger.info("POST /api/login")

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']): # Uses check_password_hash internally
        return jsonify({'error': 'Invalid email or password'}), 401

    # Generate JWT token using SECRET_KEY from app config
    try:
        secret_key = current_app.config['SECRET_KEY']
        if not secret_key:
             current_app.logger.error("JWT_SECRET_KEY is not configured!")
             return jsonify({'error': 'Authentication system configuration error'}), 500

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1) # Use timezone aware now
        }, secret_key, algorithm='HS256')

        current_app.logger.info(f"User {user.email} logged in successfully.")
        return jsonify({
            'token': token,
            'user_id': user.id,
            'email': user.email
        })
    except Exception as e:
         current_app.logger.error(f"Error generating JWT for user {data.get('email')}: {e}", exc_info=True)
         return jsonify({'error': 'Failed to process login'}), 500


@bp.route('/verify-token', methods=['POST'])
def verify_token():
    token = request.json.get('token')
    current_app.logger.info("POST /api/verify-token")

    if not token:
        return jsonify({'error': 'Token is required'}), 400

    try:
        secret_key = current_app.config['SECRET_KEY']
        if not secret_key:
             current_app.logger.error("JWT_SECRET_KEY is not configured!")
             return jsonify({'error': 'Authentication system configuration error'}), 500

        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        user = db.session.get(User, payload['user_id']) # Use newer get() method

        if not user:
            return jsonify({'error': 'User not found'}), 404

        current_app.logger.info(f"Token verified successfully for user {user.email}")
        return jsonify({
            'valid': True,
            'user_id': user.id,
            'email': user.email
        })

    except jwt.ExpiredSignatureError:
        current_app.logger.info("Token verification failed: Expired")
        return jsonify({'error': 'Token has expired', 'valid': False}), 401
    except jwt.InvalidTokenError as e:
        current_app.logger.info(f"Token verification failed: Invalid ({e})")
        return jsonify({'error': 'Invalid token', 'valid': False}), 401
    except Exception as e:
         current_app.logger.error(f"Unexpected error during token verification: {e}", exc_info=True)
         return jsonify({'error': 'Token verification failed'}), 500