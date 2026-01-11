from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from marshmallow import ValidationError
import os
import logging

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    # Set up JWT callbacks
    from app.utils.auth import setup_jwt_callbacks
    setup_jwt_callbacks(jwt)
    
    # Configure CORS - Allow all origins during development
    CORS(app, origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003"], supports_credentials=True)
    
    # Security headers
    @app.after_request
    def after_request(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
    
    # Global error handlers
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        """Handle Marshmallow validation errors"""
        return jsonify({
            'error': 'Validation Error',
            'message': 'Invalid input data',
            'details': e.messages
        }), 400
    
    @app.errorhandler(400)
    def handle_bad_request(e):
        """Handle bad request errors"""
        return jsonify({
            'error': 'Bad Request',
            'message': 'The request could not be understood by the server'
        }), 400
    
    @app.errorhandler(401)
    def handle_unauthorized(e):
        """Handle unauthorized errors"""
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication required'
        }), 401
    
    @app.errorhandler(403)
    def handle_forbidden(e):
        """Handle forbidden errors"""
        return jsonify({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource'
        }), 403
    
    @app.errorhandler(404)
    def handle_not_found(e):
        """Handle not found errors"""
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        """Handle method not allowed errors"""
        return jsonify({
            'error': 'Method Not Allowed',
            'message': 'The method is not allowed for the requested URL'
        }), 405
    
    @app.errorhandler(500)
    def handle_internal_error(e):
        """Handle internal server errors"""
        # Log the error for debugging
        app.logger.error(f'Internal server error: {str(e)}')
        
        # Don't expose internal error details in production
        if app.config.get('DEBUG'):
            return jsonify({
                'error': 'Internal Server Error',
                'message': str(e)
            }), 500
        else:
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred'
            }), 500
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        """Handle any unexpected errors"""
        # Log the error
        app.logger.error(f'Unexpected error: {str(e)}')
        
        # Return generic error message
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500
    
    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.books import books_bp
    from app.routes.exchanges import exchanges_bp
    from app.routes.recommendations import recommendations_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(books_bp, url_prefix='/api/books')
    app.register_blueprint(exchanges_bp, url_prefix='/api/exchanges')
    app.register_blueprint(recommendations_bp, url_prefix='/api')
    
    # Register admin blueprint if it exists
    try:
        from app.routes.admin import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/api/admin')
    except ImportError:
        pass
    
    # Import models to ensure they're registered
    from app.models import user, book, exchange_request, user_interaction
    
    return app