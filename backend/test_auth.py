#!/usr/bin/env python3
"""
Test script for authentication endpoints
"""
import requests
import json

def test_registration():
    """Test user registration"""
    url = "http://localhost:5000/api/auth/register"
    data = {
        "email": "test4@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            return response.json()
        else:
            print("❌ Registration failed!")
            return None
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        return None

def test_login(email="admin@bookexchange.com", password="password123"):
    """Test user login"""
    url = "http://localhost:5000/api/auth/login"
    data = {
        "email": email,
        "password": password
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            return response.json()
        else:
            print("❌ Login failed!")
            return None
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        return None

if __name__ == "__main__":
    print("Testing Authentication Endpoints...")
    print("\n1. Testing Registration:")
    test_registration()
    
    print("\n2. Testing Login with existing user:")
    test_login()