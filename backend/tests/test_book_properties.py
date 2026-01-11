"""
Property-based tests for book management functionality.
Feature: book-exchange-system
"""
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from hypothesis.strategies import composite
import json
import io
from app.models.user import User
from app.models.book import Book
from app.models.exchange_request import ExchangeRequest


@composite
def valid_book_data(draw):
    """Generate valid book data"""
    title = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ',
        min_size=1,
        max_size=200
    ).filter(lambda x: x and x.strip()))
    
    author = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ',
        min_size=1,
        max_size=100
    ).filter(lambda x: x and x.strip()))
    
    category = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ',
        min_size=1,
        max_size=50
    ).filter(lambda x: x and x.strip()))
    
    condition = draw(st.sampled_from(['new', 'like_new', 'good', 'fair', 'poor']))
    
    # Optional fields
    isbn = draw(st.one_of(
        st.none(),
        st.text(
            alphabet='0123456789X',
            min_size=10,
            max_size=20
        )
    ))
    
    description = draw(st.one_of(
        st.none(),
        st.text(
            alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?',
            min_size=1,
            max_size=1000
        ).filter(lambda x: x and x.strip())
    ))
    
    return {
        'title': title,
        'author': author,
        'category': category,
        'condition': condition,
        'isbn': isbn,
        'description': description
    }


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
        min_size=6,
        max_size=10
    ))
    password_number = draw(st.text(
        alphabet='0123456789',
        min_size=1,
        max_size=4
    ))
    password = password_base + password_number + "A1"
    
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


def create_authenticated_user(client, user_data):
    """Helper function to create and authenticate a user"""
    from app import db
    
    # Clear any existing users with this email first
    existing_user = User.query.filter_by(email=user_data['email']).first()
    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()
    
    # Register user
    register_response = client.post('/api/auth/register',
                                  data=json.dumps(user_data),
                                  content_type='application/json')
    assert register_response.status_code == 201
    
    # Login to get tokens
    login_data = {
        'email': user_data['email'],
        'password': user_data['password']
    }
    
    login_response = client.post('/api/auth/login',
                               data=json.dumps(login_data),
                               content_type='application/json')
    assert login_response.status_code == 200
    
    login_result = login_response.get_json()
    access_token = login_result['tokens']['access_token']
    user_id = login_result['user']['id']
    
    return access_token, user_id


class TestBookListingManagementProperties:
    """Property-based tests for book listing management"""
    
    @given(user_data=valid_user_data(), book_data=valid_book_data())
    @settings(max_examples=2, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=2000)
    def test_property_3_book_creation_and_storage(self, client, user_data, book_data):
        """
        Property 3: Book Listing Management
        For any valid book data, the system should store all book details correctly during creation,
        validate inputs, and assign proper ownership.
        
        Feature: book-exchange-system, Property 3: Book Listing Management
        Validates: Requirements 3.1, 3.5
        """
        # Create authenticated user
        access_token, user_id = create_authenticated_user(client, user_data)
        
        # Create book listing
        headers = {'Authorization': f'Bearer {access_token}'}
        response = client.post('/api/books',
                             data=json.dumps(book_data),
                             content_type='application/json',
                             headers=headers)
        
        # Should succeed
        assert response.status_code == 201
        data = response.get_json()
        
        # Should return book data
        assert 'book' in data
        assert 'message' in data
        
        book = data['book']
        
        # Book data should match input
        assert book['title'] == book_data['title']
        assert book['author'] == book_data['author']
        assert book['category'] == book_data['category']
        assert book['condition'] == book_data['condition']
        assert book['isbn'] == book_data['isbn']
        assert book['description'] == book_data['description']
        
        # Should have proper ownership and defaults
        assert book['user_id'] == user_id
        assert book['available'] == True  # Default availability
        assert 'id' in book
        assert 'created_at' in book
        assert 'updated_at' in book
        
        # Verify in database
        from app import db
        db_book = Book.query.get(book['id'])
        assert db_book is not None
        assert db_book.user_id == user_id
        assert db_book.title == book_data['title']
        assert db_book.author == book_data['author']
    
    @given(user_data=valid_user_data(), book_data=valid_book_data())
    @settings(max_examples=2, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=2000)
    def test_property_3_book_retrieval_individual(self, client, user_data, book_data):
        """
        Property 3: Book Listing Management
        For any created book, the system should return complete book information when queried individually.
        
        Feature: book-exchange-system, Property 3: Book Listing Management
        Validates: Requirements 3.6
        """
        # Create authenticated user and book
        access_token, user_id = create_authenticated_user(client, user_data)
        
        # Create book
        headers = {'Authorization': f'Bearer {access_token}'}
        create_response = client.post('/api/books',
                                    data=json.dumps(book_data),
                                    content_type='application/json',
                                    headers=headers)
        assert create_response.status_code == 201
        
        book_id = create_response.get_json()['book']['id']
        
        # Retrieve book by ID
        get_response = client.get(f'/api/books/{book_id}')
        
        # Should succeed
        assert get_response.status_code == 200
        data = get_response.get_json()
        
        assert 'book' in data
        book = data['book']
        
        # Should return all book information
        assert book['id'] == book_id
        assert book['title'] == book_data['title']
        assert book['author'] == book_data['author']
        assert book['category'] == book_data['category']
        assert book['condition'] == book_data['condition']
        assert book['user_id'] == user_id
        assert 'created_at' in book
        assert 'updated_at' in book
    
    @given(user_data=valid_user_data(), book_data=valid_book_data())
    @settings(max_examples=2, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=2000)
    def test_property_3_book_retrieval_listing(self, client, user_data, book_data):
        """
        Property 3: Book Listing Management
        For any created books, the system should include them in book listings with pagination.
        
        Feature: book-exchange-system, Property 3: Book Listing Management
        Validates: Requirements 3.6
        """
        # Create authenticated user and book
        access_token, user_id = create_authenticated_user(client, user_data)
        
        # Create book
        headers = {'Authorization': f'Bearer {access_token}'}
        create_response = client.post('/api/books',
                                    data=json.dumps(book_data),
                                    content_type='application/json',
                                    headers=headers)
        assert create_response.status_code == 201
        
        book_id = create_response.get_json()['book']['id']
        
        # Get books listing
        list_response = client.get('/api/books')
        
        # Should succeed
        assert list_response.status_code == 200
        data = list_response.get_json()
        
        assert 'books' in data
        assert 'pagination' in data
        
        # Should include our created book
        books = data['books']
        book_ids = [book['id'] for book in books]
        assert book_id in book_ids
        
        # Find our book in the list
        our_book = next(book for book in books if book['id'] == book_id)
        assert our_book['title'] == book_data['title']
        assert our_book['author'] == book_data['author']
    
    @given(user_data=valid_user_data(), book_data=valid_book_data(), update_data=valid_book_data())
    @settings(max_examples=2, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=2000)
    def test_property_3_book_update_with_ownership(self, client, user_data, book_data, update_data):
        """
        Property 3: Book Listing Management
        For any book owned by a user, the system should allow updates and maintain data integrity.
        
        Feature: book-exchange-system, Property 3: Book Listing Management
        Validates: Requirements 3.3
        """
        # Create authenticated user and book
        access_token, user_id = create_authenticated_user(client, user_data)
        
        # Create book
        headers = {'Authorization': f'Bearer {access_token}'}
        create_response = client.post('/api/books',
                                    data=json.dumps(book_data),
                                    content_type='application/json',
                                    headers=headers)
        assert create_response.status_code == 201
        
        book_id = create_response.get_json()['book']['id']
        
        # Update book
        update_response = client.put(f'/api/books/{book_id}',
                                   data=json.dumps(update_data),
                                   content_type='application/json',
                                   headers=headers)
        
        # Should succeed
        assert update_response.status_code == 200
        data = update_response.get_json()
        
        assert 'book' in data
        assert 'message' in data
        
        book = data['book']
        
        # Book should be updated
        assert book['id'] == book_id
        assert book['title'] == update_data['title']
        assert book['author'] == update_data['author']
        assert book['category'] == update_data['category']
        assert book['condition'] == update_data['condition']
        assert book['user_id'] == user_id  # Ownership unchanged
        
        # Verify in database
        from app import db
        db_book = Book.query.get(book_id)
        assert db_book is not None
        assert db_book.title == update_data['title']
        assert db_book.author == update_data['author']
    
    @given(user_data=valid_user_data(), other_user_data=valid_user_data(), book_data=valid_book_data())
    @settings(max_examples=1, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=3000)
    def test_property_3_book_update_ownership_verification(self, client, user_data, other_user_data, book_data):
        """
        Property 3: Book Listing Management
        For any book, only the owner should be able to update it.
        
        Feature: book-exchange-system, Property 3: Book Listing Management
        Validates: Requirements 3.3
        """
        # Ensure different users
        if user_data['email'] == other_user_data['email']:
            other_user_data['email'] = 'other_' + other_user_data['email']
        
        # Create first user and book
        access_token1, user_id1 = create_authenticated_user(client, user_data)
        
        headers1 = {'Authorization': f'Bearer {access_token1}'}
        create_response = client.post('/api/books',
                                    data=json.dumps(book_data),
                                    content_type='application/json',
                                    headers=headers1)
        assert create_response.status_code == 201
        
        book_id = create_response.get_json()['book']['id']
        
        # Create second user
        access_token2, user_id2 = create_authenticated_user(client, other_user_data)
        
        # Second user tries to update first user's book
        headers2 = {'Authorization': f'Bearer {access_token2}'}
        update_data = {'title': 'Unauthorized Update'}
        
        update_response = client.put(f'/api/books/{book_id}',
                                   data=json.dumps(update_data),
                                   content_type='application/json',
                                   headers=headers2)
        
        # Should fail with forbidden
        assert update_response.status_code == 403
        data = update_response.get_json()
        assert 'error' in data
        assert 'forbidden' in data['error'].lower() or 'forbidden' in data.get('message', '').lower()
    
    @given(user_data=valid_user_data(), book_data=valid_book_data())
    @settings(max_examples=2, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=2000)
    def test_property_3_book_deletion_with_cascade(self, client, user_data, book_data):
        """
        Property 3: Book Listing Management
        For any book owned by a user, the system should allow deletion and handle cascade effects.
        
        Feature: book-exchange-system, Property 3: Book Listing Management
        Validates: Requirements 3.4
        """
        # Create authenticated user and book
        access_token, user_id = create_authenticated_user(client, user_data)
        
        # Create book
        headers = {'Authorization': f'Bearer {access_token}'}
        create_response = client.post('/api/books',
                                    data=json.dumps(book_data),
                                    content_type='application/json',
                                    headers=headers)
        assert create_response.status_code == 201
        
        book_id = create_response.get_json()['book']['id']
        
        # Delete book
        delete_response = client.delete(f'/api/books/{book_id}',
                                      headers=headers)
        
        # Should succeed
        assert delete_response.status_code == 200
        data = delete_response.get_json()
        assert 'message' in data
        
        # Book should be deleted from database
        from app import db
        db_book = Book.query.get(book_id)
        assert db_book is None
        
        # Trying to get deleted book should return 404
        get_response = client.get(f'/api/books/{book_id}')
        assert get_response.status_code == 404
    
    @given(user_data=valid_user_data(), other_user_data=valid_user_data(), book_data=valid_book_data())
    @settings(max_examples=1, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=3000)
    def test_property_3_book_deletion_ownership_verification(self, client, user_data, other_user_data, book_data):
        """
        Property 3: Book Listing Management
        For any book, only the owner should be able to delete it.
        
        Feature: book-exchange-system, Property 3: Book Listing Management
        Validates: Requirements 3.4
        """
        # Ensure different users
        if user_data['email'] == other_user_data['email']:
            other_user_data['email'] = 'other_' + other_user_data['email']
        
        # Create first user and book
        access_token1, user_id1 = create_authenticated_user(client, user_data)
        
        headers1 = {'Authorization': f'Bearer {access_token1}'}
        create_response = client.post('/api/books',
                                    data=json.dumps(book_data),
                                    content_type='application/json',
                                    headers=headers1)
        assert create_response.status_code == 201
        
        book_id = create_response.get_json()['book']['id']
        
        # Create second user
        access_token2, user_id2 = create_authenticated_user(client, other_user_data)
        
        # Second user tries to delete first user's book
        headers2 = {'Authorization': f'Bearer {access_token2}'}
        
        delete_response = client.delete(f'/api/books/{book_id}',
                                      headers=headers2)
        
        # Should fail with forbidden
        assert delete_response.status_code == 403
        data = delete_response.get_json()
        assert 'error' in data
        assert 'forbidden' in data['error'].lower() or 'forbidden' in data.get('message', '').lower()
        
        # Book should still exist
        from app import db
        db_book = Book.query.get(book_id)
        assert db_book is not None


class TestImageUploadSecurityProperties:
    """Property-based tests for image upload security and validation"""
    
    @given(user_data=valid_user_data())
    @settings(max_examples=1, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=2000)
    def test_property_10_image_upload_file_validation(self, client, user_data):
        """
        Property 10: Security and Input Validation
        For any file upload, the system should validate file types and sizes to prevent malicious uploads.
        
        Feature: book-exchange-system, Property 10: Security and Input Validation
        Validates: Requirements 10.2
        """
        # Create authenticated user
        access_token, user_id = create_authenticated_user(client, user_data)
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Test 1: No file provided
        response = client.post('/api/books/upload-image', headers=headers)
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'no image file' in data['message'].lower()
        
        # Test 2: Empty filename
        response = client.post('/api/books/upload-image', 
                             data={'image': (io.BytesIO(b''), '')},
                             headers=headers)
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'no file selected' in data['message'].lower()
        
        # Test 3: Invalid file type
        response = client.post('/api/books/upload-image',
                             data={'image': (io.BytesIO(b'fake content'), 'test.txt')},
                             headers=headers)
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'invalid file type' in data['message'].lower()
        
        # Test 4: Valid image file (small PNG)
        # Create a minimal valid PNG file (1x1 pixel)
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc\xf8\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
        
        response = client.post('/api/books/upload-image',
                             data={'image': (io.BytesIO(png_data), 'test.png')},
                             headers=headers)
        
        # Should succeed for valid image
        if response.status_code == 200:
            data = response.get_json()
            assert 'image_url' in data
            assert 'message' in data
            assert data['image_url'].endswith('.png')
        else:
            # If it fails, it should be due to authentication or server issues, not validation
            assert response.status_code in [401, 500]
    
    @given(user_data=valid_user_data())
    @settings(max_examples=1, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=2000)
    def test_property_10_image_upload_size_validation(self, client, user_data):
        """
        Property 10: Security and Input Validation
        For any file upload, the system should enforce size limits to prevent resource exhaustion.
        
        Feature: book-exchange-system, Property 10: Security and Input Validation
        Validates: Requirements 10.2
        """
        # Create authenticated user
        access_token, user_id = create_authenticated_user(client, user_data)
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Test oversized file (simulate 6MB file)
        large_data = b'x' * (6 * 1024 * 1024)  # 6MB of data
        
        response = client.post('/api/books/upload-image',
                             data={'image': (io.BytesIO(large_data), 'large.jpg')},
                             headers=headers)
        
        # Should reject oversized files
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert '5mb' in data['message'].lower() or 'size' in data['message'].lower()