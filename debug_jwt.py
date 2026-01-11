#!/usr/bin/env python3
"""
Debug JWT token issues
"""

import requests
import json
import jwt as pyjwt

API_BASE = 'http://localhost:5000/api'

def debug_jwt_token():
    print("🔍 Debugging JWT Token Issues\n")
    
    # Step 1: Login to get token
    print("1. Getting fresh token...")
    login_data = {
        'email': 'frontend_api_test@example.com',
        'password': 'TestPass123'
    }
    
    try:
        response = requests.post(
            f'{API_BASE}/auth/login',
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code != 200:
            print(f"   ❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
            
        tokens = response.json()['tokens']
        access_token = tokens['access_token']
        print(f"   ✅ Got access token: {access_token[:50]}...")
        
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return
    
    # Step 2: Decode token to see contents
    print("\n2. Decoding token...")
    try:
        # Decode without verification to see contents
        decoded = pyjwt.decode(access_token, options={"verify_signature": False})
        print(f"   Token contents: {json.dumps(decoded, indent=2)}")
        
    except Exception as e:
        print(f"   ❌ Token decode error: {e}")
    
    # Step 3: Test profile with different header formats
    print("\n3. Testing profile access with different header formats...")
    
    # Format 1: Bearer token
    print("   Testing with 'Bearer' prefix...")
    try:
        response = requests.get(
            f'{API_BASE}/auth/profile',
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
        )
        print(f"   Status: {response.status_code}")
        if response.status_code != 200:
            print(f"   Response: {response.text}")
        else:
            print(f"   ✅ Success with Bearer prefix")
            
    except Exception as e:
        print(f"   ❌ Bearer format error: {e}")
    
    # Format 2: Without Bearer prefix
    print("   Testing without 'Bearer' prefix...")
    try:
        response = requests.get(
            f'{API_BASE}/auth/profile',
            headers={
                'Authorization': access_token,
                'Content-Type': 'application/json'
            }
        )
        print(f"   Status: {response.status_code}")
        if response.status_code != 200:
            print(f"   Response: {response.text}")
        else:
            print(f"   ✅ Success without Bearer prefix")
            
    except Exception as e:
        print(f"   ❌ No Bearer format error: {e}")
    
    # Step 4: Check if token is in blacklist
    print("\n4. Testing token blacklist...")
    try:
        # Make multiple requests to see if token gets blacklisted
        for i in range(3):
            response = requests.get(
                f'{API_BASE}/auth/profile',
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }
            )
            print(f"   Request {i+1}: Status {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Blacklist test error: {e}")

if __name__ == '__main__':
    debug_jwt_token()