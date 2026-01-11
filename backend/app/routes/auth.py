from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.user import User
from app.utils.auth import hash_password, verify_password, generate_tokens, blacklist_token
from app.schemas.auth import registration_schema, login_schema

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        # Validate input data
        data = registration_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({
            'error': 'Validation Error',
            'message': 'Invalid input data',
            'details': err.messages
        }), 400
    
    try:
        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({
                'error': 'Registration Failed',
                'message': 'User with this email already exists'
            }), 409
        
        # Hash password
        password_hash = hash_password(data['password'])
        
        # Create new user
        new_user = User(
            email=data['email'],
            password_hash=password_hash,
            first_name=data['first_name'],
            last_name=data['last_name'],
            role='user'  # Default role
        )
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        # Generate tokens
        tokens = generate_tokens(new_user.id, new_user.role)
        
        return jsonify({
            'message': 'User registered successfully',
            'user': new_user.to_dict(),
            'tokens': tokens
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'error': 'Registration Failed',
            'message': 'User with this email already exists'
        }), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Registration Failed',
            'message': 'An unexpected error occurred'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        # Validate input data
        data = login_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({
            'error': 'Validation Error',
            'message': 'Invalid input data',
            'details': err.messages
        }), 400
    
    try:
        # Find user by email
        user = User.query.filter_by(email=data['email']).first()
        
        if not user:
            return jsonify({
                'error': 'Authentication Failed',
                'message': 'Invalid email or password'
            }), 401
        
        # Verify password
        if not verify_password(data['password'], user.password_hash):
            return jsonify({
                'error': 'Authentication Failed',
                'message': 'Invalid email or password'
            }), 401
        
        # Generate tokens
        tokens = generate_tokens(user.id, user.role)
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'tokens': tokens
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Login Failed',
            'message': 'An unexpected error occurred'
        }), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Token refresh endpoint"""
    try:
        # Get current user from refresh token
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        user_role = claims.get('role', 'user')
        
        # Convert string back to int for token generation
        user_id = int(current_user_id)
        
        # Generate new access token
        new_tokens = generate_tokens(user_id, user_role)
        
        return jsonify({
            'message': 'Token refreshed successfully',
            'tokens': new_tokens
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Token Refresh Failed',
            'message': 'Unable to refresh token'
        }), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        current_user_id = get_jwt_identity()
        # Convert string back to int for database query
        user_id = int(current_user_id)
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'error': 'User Not Found',
                'message': 'User profile not found'
            }), 404
        
        return jsonify({
            'message': 'Profile retrieved successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Profile Retrieval Failed',
            'message': 'Unable to retrieve profile'
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """User logout endpoint"""
    try:
        # Get token JTI for blacklisting
        jti = get_jwt()['jti']
        
        # Add token to blacklist
        blacklist_token(jti)
        
        return jsonify({
            'message': 'Successfully logged out'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Logout Failed',
            'message': 'An unexpected error occurred'
        }), 500