#!/usr/bin/env python3
"""
Test script to verify frontend-backend communication
This mimics what the frontend JavaScript should be doing
"""

import requests
import json

API_BASE = 'http://localhost:5000/api'

def test_frontend_api():
    print("🔍 Testing Frontend-Backend API Communication\n")
    
    # Test 1: Registration
    print("1. Testing Registration...")
    register_data = {
        'email': 'new_frontend_test@example.com',
        'password': 'TestPass123',
        'first_name': 'New',
        'last_name': 'Frontend'
    }
    
    try:
        response = requests.post(
            f'{API_BASE}/auth/register',
            json=register_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 201:
            print("   ✅ Registration successful")
            tokens = response.json()['tokens']
            access_token = tokens['access_token']
        else:
            print("   ❌ Registration failed")
            return
            
    except Exception as e:
        print(f"   ❌ Registration error: {e}")
        return
    
    # Test 2: Login
    print("\n2. Testing Login...")
    login_data = {
        'email': 'new_frontend_test@example.com',
        'password': 'TestPass123'
    }
    
    try:
        response = requests.post(
            f'{API_BASE}/auth/login',
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            print("   ✅ Login successful")
            tokens = response.json()['tokens']
            access_token = tokens['access_token']
        else:
            print("   ❌ Login failed")
            return
            
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return
    
    # Test 3: Profile Access
    print("\n3. Testing Profile Access...")
    try:
        response = requests.get(
            f'{API_BASE}/auth/profile',
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            print("   ✅ Profile access successful")
        else:
            print("   ❌ Profile access failed")
            
    except Exception as e:
        print(f"   ❌ Profile error: {e}")
    
    # Test 4: CORS Preflight (OPTIONS request)
    print("\n4. Testing CORS Preflight...")
    try:
        response = requests.options(
            f'{API_BASE}/auth/login',
            headers={
                'Origin': 'http://localhost:3003',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   CORS Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("   ✅ CORS preflight successful")
        else:
            print("   ❌ CORS preflight failed")
            
    except Exception as e:
        print(f"   ❌ CORS error: {e}")
    
    print("\n🎉 API tests completed!")
    print("\nIf all tests passed, the backend is working correctly.")
    print("If frontend login is still failing, check:")
    print("1. Browser console for JavaScript errors")
    print("2. Network tab for failed requests")
    print("3. Frontend is connecting to the right API URL")

if __name__ == '__main__':
    test_frontend_api()