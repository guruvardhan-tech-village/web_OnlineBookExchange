"""
Authentication utilities for password hashing and verification.
"""
import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with a secure salt.
    
    Args:
        password (str): The plain text password to hash
        
    Returns:
        str: The hashed password as a string
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    # Return as string for database storage
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        password (str): The plain text password to verify
        hashed_password (str): The stored hashed password
        
    Returns:
        bool: True if password matches, False otherwise
    """
    if not password or not hashed_password:
        return False
    
    try:
        # Convert string back to bytes for bcrypt
        return bcrypt.checkpw(
            password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )
    except (ValueError, TypeError):
        return False


from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt
from datetime import timedelta


# Token blacklist - in production, use Redis or database
blacklisted_tokens = set()


def generate_tokens(user_id: int, role: str = 'user') -> dict:
    """
    Generate access and refresh tokens for a user.
    
    Args:
        user_id (int): The user's ID
        role (str): The user's role (default: 'user')
        
    Returns:
        dict: Dictionary containing access_token and refresh_token
    """
    additional_claims = {"role": role}
    
    # Convert user_id to string for JWT subject
    user_identity = str(user_id)
    
    access_token = create_access_token(
        identity=user_identity,
        additional_claims=additional_claims
    )
    
    refresh_token = create_refresh_token(
        identity=user_identity,
        additional_claims=additional_claims
    )
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


def blacklist_token(jti: str) -> None:
    """
    Add a token to the blacklist.
    
    Args:
        jti (str): The JWT ID (jti) of the token to blacklist
    """
    blacklisted_tokens.add(jti)


def is_token_blacklisted(jti: str) -> bool:
    """
    Check if a token is blacklisted.
    
    Args:
        jti (str): The JWT ID (jti) to check
        
    Returns:
        bool: True if token is blacklisted, False otherwise
    """
    return jti in blacklisted_tokens


def setup_jwt_callbacks(jwt_manager):
    """
    Set up JWT callbacks for token validation and blacklisting.
    
    Args:
        jwt_manager: The Flask-JWT-Extended JWTManager instance
    """
    
    @jwt_manager.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        """Check if token is in blacklist"""
        jti = jwt_payload['jti']
        return is_token_blacklisted(jti)
    
    @jwt_manager.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """Return message when token is revoked"""
        return {
            'error': 'Token has been revoked',
            'message': 'Please log in again'
        }, 401
    
    @jwt_manager.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Return message when token is expired"""
        return {
            'error': 'Token has expired',
            'message': 'Please refresh your token or log in again'
        }, 401
    
    @jwt_manager.invalid_token_loader
    def invalid_token_callback(error):
        """Return message when token is invalid"""
        return {
            'error': 'Invalid token',
            'message': 'Please provide a valid token'
        }, 401
    
    @jwt_manager.unauthorized_loader
    def missing_token_callback(error):
        """Return message when token is missing"""
        return {
            'error': 'Authorization token required',
            'message': 'Please provide a valid token'
        }, 401

from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request, get_jwt_identity


def admin_required(f):
    """
    Decorator to require admin role for accessing an endpoint.
    
    Usage:
        @admin_required
        def admin_only_endpoint():
            pass
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verify JWT token is present and valid
        verify_jwt_in_request()
        
        # Get claims from token
        claims = get_jwt()
        user_role = claims.get('role', 'user')
        
        # Check if user has admin role
        if user_role != 'admin':
            return {
                'error': 'Access Denied',
                'message': 'Admin privileges required'
            }, 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def role_required(required_role):
    """
    Decorator factory to require specific role for accessing an endpoint.
    
    Usage:
        @role_required('admin')
        def admin_endpoint():
            pass
            
        @role_required('user')
        def user_endpoint():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verify JWT token is present and valid
            verify_jwt_in_request()
            
            # Get claims from token
            claims = get_jwt()
            user_role = claims.get('role', 'user')
            
            # Check if user has required role
            if user_role != required_role:
                return {
                    'error': 'Access Denied',
                    'message': f'{required_role.title()} privileges required'
                }, 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def get_current_user():
    """
    Get the current authenticated user from JWT token.
    
    Returns:
        User: The current user object or None if not found
    """
    try:
        verify_jwt_in_request()
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str)
        
        from app.models.user import User
        return User.query.get(user_id)
    except:
        return None


def get_current_user_id():
    """
    Get the current authenticated user ID from JWT token.
    
    Returns:
        int: The current user ID or None if not authenticated
    """
    try:
        verify_jwt_in_request()
        user_id_str = get_jwt_identity()
        return int(user_id_str)
    except:
        return None