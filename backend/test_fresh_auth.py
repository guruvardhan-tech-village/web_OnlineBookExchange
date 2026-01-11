#!/usr/bin/env python3
"""
Test authentication with fresh Flask app instance
"""
import os
import pymysql
from dotenv import load_dotenv

# Use PyMySQL as MySQL driver
pymysql.install_as_MySQLdb()

# Load environment variables
load_dotenv()

from app import create_app
import requests
import json

def test_with_fresh_app():
    """Test authentication with a fresh Flask app"""
    app = create_app()
    
    # Start test client
    with app.test_client() as client:
        # Test registration
        print("Testing registration...")
        response = client.post('/api/auth/register', 
                             json={
                                 "email": "test5@example.com",
                                 "password": "password123",
                                 "first_name": "Test",
                                 "last_name": "User"
                             },
                             content_type='application/json')
        
        print(f"Registration Status: {response.status_code}")
        print(f"Registration Response: {response.get_json()}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
        else:
            print("❌ Registration failed!")
        
        # Test login with existing user
        print("\nTesting login...")
        response = client.post('/api/auth/login',
                             json={
                                 "email": "admin@bookexchange.com",
                                 "password": "password123"
                             },
                             content_type='application/json')
        
        print(f"Login Status: {response.status_code}")
        print(f"Login Response: {response.get_json()}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
        else:
            print("❌ Login failed!")

if __name__ == "__main__":
    test_with_fresh_app()