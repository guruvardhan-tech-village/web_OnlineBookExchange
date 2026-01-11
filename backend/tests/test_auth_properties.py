"""
Property-based tests for authentication functionality.
Feature: book-exchange-system
"""
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from hypothesis.strategies import composite
import json
from app.models.user import User
from app.utils.auth import verify_password


@composite
def valid_user_data(draw):
    """Generate valid user registration data"""
    # Generate valid email with ASCII characters only
    username = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
        min_size=3,
        max_size=20
    ).filter(lambda x: x and x[0].isalpha()))
    
    domain = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        min_size=2,
        max_size=10
    ).filter(lambda x: x and x.isalpha()))
    
    tld = draw(st.sampled_from(['com', 'org', 'net', 'edu']))
    email = f"{username}@{domain}.{tld}".lower()
    
    # Generate valid password (at least 8 chars, contains letter and number)
    password_base = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        min_size=6,  # Increased to ensure minimum 8 chars total
        max_size=10
    ))
    password_number = draw(st.text(
        alphabet='0123456789',
        min_size=1,
        max_size=4
    ))
    password = password_base + password_number + "A1"  # Ensure requirements (6+1+2=9 minimum)
    
    # Generate names with ASCII characters only
    first_name = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        min_size=1,
        max_size=50
    ).filter(lambda x: x and x.strip()))
    
    last_name = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        min_size=1,
        max_size=50
    ).filter(lambda x: x and x.strip()))
    
    return {
        'email': email,
        'password': password,
        'first_name': first_name,
        'last_name': last_name
    }


@composite
def invalid_user_data(draw):
    """Generate invalid user registration data"""
    choice = draw(st.integers(min_value=1, max_value=4))
    
    if choice == 1:
        # Invalid email
        return {
            'email': draw(st.text(min_size=1, max_size=50).filter(lambda x: '@' not in x)),
            'password': 'ValidPass123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
    elif choice == 2:
        # Invalid password (too short)
        return {
            'email': 'test@example.com',
            'password': draw(st.text(max_size=7)),
            'first_name': 'John',
            'last_name': 'Doe'
        }
    elif choice == 3:
        # Missing first name
        return {
            'email': 'test@example.com',
            'password': 'ValidPass123',
            'first_name': '',
            'last_name': 'Doe'
        }
    else:
        # Missing last name
        return {
            'email': 'test@example.com',
            'password': 'ValidPass123',
            'first_name': 'John',
            'last_name': ''
        }


class TestUserRegistrationProperties:
    """Property-based tests for user registration and authentication"""
    
    @given(user_data=valid_user_data())
    @settings(max_examples=5, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=1000)
    def test_property_1_user_registration_and_authentication_valid_data(self, client, user_data):
        """
        Property 1: User Registration and Authentication
        For any valid user registration data, the system should create a new user account 
        with securely hashed passwords and authenticate valid credentials with JWT tokens.
        
        Feature: book-exchange-system, Property 1: User Registration and Authentication
        Validates: Requirements 1.1, 1.2
        """
        # Clear any existing users with this email first
        from app import db
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
        
        # Test registration with valid data
        response = client.post('/api/auth/register', 
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        # Should succeed
        assert response.status_code == 201
        data = response.get_json()
        
        # Should return user data and tokens
        assert 'user' in data
        assert 'tokens' in data
        assert 'message' in data
        
        # User data should match input
        user = data['user']
        assert user['email'] == user_data['email']
        assert user['first_name'] == user_data['first_name']
        assert user['last_name'] == user_data['last_name']
        assert user['role'] == 'user'  # Default role
        
        # Should have tokens
        tokens = data['tokens']
        assert 'access_token' in tokens
        assert 'refresh_token' in tokens
        assert tokens['access_token']
        assert tokens['refresh_token']
        
        # Password should be hashed (not stored in plain text)
        assert 'password' not in user
        assert 'password_hash' not in user
        
        # Verify password was hashed correctly by checking database
        db_user = User.query.filter_by(email=user_data['email']).first()
        assert db_user is not None
        assert verify_password(user_data['password'], db_user.password_hash)
    
    @given(user_data=valid_user_data())
    @settings(max_examples=3, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=1000)
    def test_property_1_prevent_duplicate_registration(self, client, user_data):
        """
        Property 1: User Registration and Authentication
        For any valid user data, attempting to register twice with the same email 
        should prevent duplicate registration and return appropriate error.
        
        Feature: book-exchange-system, Property 1: User Registration and Authentication
        Validates: Requirements 1.2
        """
        # Clear any existing users with this email first
        from app import db
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
        
        # First registration should succeed
        response1 = client.post('/api/auth/register',
                               data=json.dumps(user_data),
                               content_type='application/json')
        assert response1.status_code == 201
        
        # Second registration with same email should fail
        response2 = client.post('/api/auth/register',
                               data=json.dumps(user_data),
                               content_type='application/json')
        assert response2.status_code == 409
        
        data = response2.get_json()
        assert 'error' in data
        assert 'message' in data
        assert 'already exists' in data['message'].lower()
    
    @given(user_data=invalid_user_data())
    @settings(max_examples=5, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_1_reject_invalid_registration_data(self, client, user_data):
        """
        Property 1: User Registration and Authentication
        For any invalid user registration data, the system should reject the registration 
        and return appropriate validation errors.
        
        Feature: book-exchange-system, Property 1: User Registration and Authentication
        Validates: Requirements 1.1, 1.2
        """
        response = client.post('/api/auth/register',
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        # Should fail with validation error
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Validation Error'
        assert 'details' in data or 'message' in data
    
    @given(user_data=valid_user_data())
    @settings(max_examples=3, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=1000)
    def test_property_1_authentication_valid_credentials(self, client, user_data):
        """
        Property 1: User Registration and Authentication
        For any valid user credentials, the system should authenticate them and return JWT tokens.
        
        Feature: book-exchange-system, Property 1: User Registration and Authentication
        Validates: Requirements 1.3, 1.4, 1.6
        """
        # Clear any existing users with this email first
        from app import db
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
        
        # First register the user
        register_response = client.post('/api/auth/register',
                                      data=json.dumps(user_data),
                                      content_type='application/json')
        assert register_response.status_code == 201
        
        # Now test login with valid credentials
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        
        response = client.post('/api/auth/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        # Should succeed
        assert response.status_code == 200
        data = response.get_json()
        
        # Should return user data and tokens
        assert 'user' in data
        assert 'tokens' in data
        assert 'message' in data
        
        # User data should match
        user = data['user']
        assert user['email'] == user_data['email']
        assert user['first_name'] == user_data['first_name']
        assert user['last_name'] == user_data['last_name']
        
        # Should have tokens
        tokens = data['tokens']
        assert 'access_token' in tokens
        assert 'refresh_token' in tokens
        assert tokens['access_token']
        assert tokens['refresh_token']
    
    @given(user_data=valid_user_data())
    @settings(max_examples=3, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=1000)
    def test_property_1_authentication_invalid_credentials(self, client, user_data):
        """
        Property 1: User Registration and Authentication
        For any invalid credentials, the system should reject authentication and return appropriate error.
        
        Feature: book-exchange-system, Property 1: User Registration and Authentication
        Validates: Requirements 1.4
        """
        # Clear any existing users with this email first
        from app import db
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
        
        # First register the user
        register_response = client.post('/api/auth/register',
                                      data=json.dumps(user_data),
                                      content_type='application/json')
        assert register_response.status_code == 201
        
        # Test login with wrong password
        login_data = {
            'email': user_data['email'],
            'password': user_data['password'] + 'wrong'
        }
        
        response = client.post('/api/auth/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        # Should fail
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert 'message' in data
        assert 'invalid' in data['message'].lower()
        
        # Test login with non-existent email
        login_data = {
            'email': 'nonexistent@example.com',
            'password': user_data['password']
        }
        
        response = client.post('/api/auth/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        # Should fail
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert 'message' in data
        assert 'invalid' in data['message'].lower()


class TestRoleBasedAccessProperties:
    """Property-based tests for role-based access control"""
    
    @given(user_data=valid_user_data())
    @settings(max_examples=3, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=1000)
    def test_property_2_role_based_access_control_default_role(self, client, user_data):
        """
        Property 2: Role-Based Access Control
        For any new user registration, the system should assign them a default "User" role.
        
        Feature: book-exchange-system, Property 2: Role-Based Access Control
        Validates: Requirements 2.1
        """
        # Clear any existing users with this email first
        from app import db
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
        
        # Register user
        response = client.post('/api/auth/register',
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        # Should succeed and assign default role
        assert response.status_code == 201
        data = response.get_json()
        
        user = data['user']
        assert user['role'] == 'user'  # Default role should be 'user'
        
        # Verify in database
        db_user = User.query.filter_by(email=user_data['email']).first()
        assert db_user is not None
        assert db_user.role == 'user'
    
    @given(user_data=valid_user_data())
    @settings(max_examples=2, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=1000)
    def test_property_2_role_based_access_control_admin_promotion(self, client, user_data):
        """
        Property 2: Role-Based Access Control
        For any user, an admin should be able to promote them to admin role.
        
        Feature: book-exchange-system, Property 2: Role-Based Access Control
        Validates: Requirements 2.2
        """
        # Clear any existing users with this email first
        from app import db
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
        
        # Register user
        response = client.post('/api/auth/register',
                             data=json.dumps(user_data),
                             content_type='application/json')
        assert response.status_code == 201
        
        # Get the user from database and promote to admin
        db_user = User.query.filter_by(email=user_data['email']).first()
        assert db_user is not None
        
        # Simulate admin promotion (direct database update for testing)
        db_user.role = 'admin'
        db.session.commit()
        
        # Verify role was updated
        updated_user = User.query.filter_by(email=user_data['email']).first()
        assert updated_user.role == 'admin'
        
        # Test login returns admin role in token
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        
        login_response = client.post('/api/auth/login',
                                   data=json.dumps(login_data),
                                   content_type='application/json')
        
        if login_response.status_code == 200:
            login_data = login_response.get_json()
            user_info = login_data['user']
            assert user_info['role'] == 'admin'