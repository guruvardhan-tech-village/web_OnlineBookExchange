#!/usr/bin/env python3
"""
Verify server is working correctly
"""
import requests
import time

def test_server_health():
    """Test if server is responding correctly"""
    try:
        # Test basic connectivity
        response = requests.get('http://localhost:5000/api/auth/profile', timeout=5)
        if response.status_code == 401:  # Expected - needs auth
            print("✅ Server is responding correctly")
            return True
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server - is it running?")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_registration():
    """Test registration endpoint"""
    try:
        response = requests.post('http://localhost:5000/api/auth/register', 
                               json={
                                   "email": f"test-{int(time.time())}@example.com",
                                   "password": "password123",
                                   "first_name": "Test",
                                   "last_name": "User"
                               },
                               timeout=10)
        
        if response.status_code == 201:
            print("✅ Registration working correctly")
            return True
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        return False

def test_login():
    """Test login with existing user"""
    try:
        response = requests.post('http://localhost:5000/api/auth/login',
                               json={
                                   "email": "admin@bookexchange.com",
                                   "password": "password123"
                               },
                               timeout=10)
        
        if response.status_code == 200:
            print("✅ Login working correctly")
            return True
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Verifying server health...")
    
    if not test_server_health():
        print("\n❌ Server is not responding. Please start the Flask server:")
        print("   cd backend")
        print("   python run.py")
        exit(1)
    
    print("\n🔍 Testing authentication endpoints...")
    
    registration_ok = test_registration()
    login_ok = test_login()
    
    if registration_ok and login_ok:
        print("\n🎉 All tests passed! Authentication is working correctly.")
        print("You can now test the frontend authentication.")
    else:
        print("\n❌ Some tests failed. Please check the server configuration.")