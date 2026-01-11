#!/usr/bin/env python3
"""
Direct JWT test using Flask app context
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.utils.auth import generate_tokens
from flask_jwt_extended import decode_token

def test_jwt_direct():
    print("🔍 Testing JWT directly in Flask context\n")
    
    app = create_app('development')
    
    with app.app_context():
        # Find a test user
        user = User.query.filter_by(email='frontend_api_test@example.com').first()
        if not user:
            print("❌ Test user not found")
            return
        
        print(f"✅ Found user: {user.email} (ID: {user.id})")
        
        # Generate tokens
        tokens = generate_tokens(user.id, user.role)
        access_token = tokens['access_token']
        
        print(f"✅ Generated token: {access_token[:50]}...")
        
        # Try to decode token using Flask-JWT-Extended
        try:
            decoded = decode_token(access_token)
            print(f"✅ Token decoded successfully: {decoded}")
        except Exception as e:
            print(f"❌ Token decode failed: {e}")
        
        # Test JWT configuration
        print(f"\nJWT Configuration:")
        print(f"  JWT_SECRET_KEY: {app.config.get('JWT_SECRET_KEY', 'NOT SET')[:20]}...")
        print(f"  JWT_CSRF_IN_COOKIES: {app.config.get('JWT_CSRF_IN_COOKIES', 'NOT SET')}")
        print(f"  JWT_CSRF_CHECK_FORM: {app.config.get('JWT_CSRF_CHECK_FORM', 'NOT SET')}")

if __name__ == '__main__':
    test_jwt_direct()