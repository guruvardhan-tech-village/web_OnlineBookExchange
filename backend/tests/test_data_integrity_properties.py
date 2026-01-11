"""
Property-based tests for data integrity and persistence functionality.
Feature: book-exchange-system
"""
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from hypothesis.strategies import composite
import json
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy import text
from app.models.user import User
from app.models.book import Book
from app.models.exchange_request import ExchangeRequest
from app.models.user_interaction import UserInteraction
from app import db


@composite
def valid_user_data(draw):
    """Generate valid user data for testing"""
    username = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
        min_size=3,
        max_size=15
    ).filter(lambda x: x and x[0].isalpha()))
    
    domain = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        min_size=2,
        max_size=8
    ).filter(lambda x: x and x.isalpha()))
    
    tld = draw(st.sampled_from(['com', 'org', 'net', 'edu']))
    email = f"{username}@{domain}.{tld}".lower()
    
    first_name = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        min_size=1,
        max_size=20
    ).filter(lambda x: x and x.strip()))
    
    last_name = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        min_size=1,
        max_size=20
    ).filter(lambda x: x and x.strip()))
    
    return {
        'email': email,
        'password_hash': 'hashed_password_123',
        'first_name': first_name,
        'last_name': last_name,
        'role': draw(st.sampled_from(['user', 'admin']))
    }


@composite
def valid_book_data(draw):
    """Generate valid book data for testing"""
    title = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ',
        min_size=1,
        max_size=50
    ).filter(lambda x: x and x.strip()))
    
    author = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ',
        min_size=1,
        max_size=30
    ).filter(lambda x: x and x.strip()))
    
    category = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        min_size=1,
        max_size=20
    ).filter(lambda x: x and x.strip()))
    
    # Generate valid ISBN (10 or 13 digits)
    isbn_length = draw(st.sampled_from([10, 13]))
    isbn = draw(st.text(
        alphabet='0123456789',
        min_size=isbn_length,
        max_size=isbn_length
    ))
    
    return {
        'title': title,
        'author': author,
        'isbn': isbn,
        'category': category,
        'condition': draw(st.sampled_from(['new', 'like_new', 'good', 'fair', 'poor'])),
        'description': draw(st.text(max_size=100)),
        'available': draw(st.booleans())
    }


@composite
def invalid_user_data(draw):
    """Generate invalid user data for constraint testing"""
    choice = draw(st.integers(min_value=1, max_value=3))
    
    if choice == 1:
        # Invalid email (no @ symbol)
        return {
            'email': draw(st.text(min_size=1, max_size=20).filter(lambda x: '@' not in x and x.strip())),
            'password_hash': 'hashed_password_123',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'user'
        }
    elif choice == 2:
        # Empty first name
        return {
            'email': 'test@example.com',
            'password_hash': 'hashed_password_123',
            'first_name': '',
            'last_name': 'Doe',
            'role': 'user'
        }
    else:
        # Empty last name
        return {
            'email': 'test@example.com',
            'password_hash': 'hashed_password_123',
            'first_name': 'John',
            'last_name': '',
            'role': 'user'
        }


@composite
def invalid_book_data(draw):
    """Generate invalid book data for constraint testing"""
    choice = draw(st.integers(min_value=1, max_value=4))
    
    if choice == 1:
        # Empty title
        return {
            'title': '',
            'author': 'Valid Author',
            'category': 'Fiction',
            'condition': 'good'
        }
    elif choice == 2:
        # Empty author
        return {
            'title': 'Valid Title',
            'author': '',
            'category': 'Fiction',
            'condition': 'good'
        }
    elif choice == 3:
        # Empty category
        return {
            'title': 'Valid Title',
            'author': 'Valid Author',
            'category': '',
            'condition': 'good'
        }
    else:
        # Invalid ISBN (too short)
        return {
            'title': 'Valid Title',
            'author': 'Valid Author',
            'category': 'Fiction',
            'condition': 'good',
            'isbn': draw(st.text(alphabet='0123456789', min_size=1, max_size=9))
        }


def clean_database():
    """Clean database state between tests"""
    try:
        # Delete in reverse dependency order to avoid foreign key constraint errors
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        UserInteraction.query.delete()
        ExchangeRequest.query.delete()
        Book.query.delete()
        User.query.delete()
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        db.session.commit()
    except Exception as e:
        print(f"Clean database error: {e}")
        db.session.rollback()
        # Try alternative cleanup method
        try:
            db.session.execute(text("TRUNCATE TABLE user_interactions"))
            db.session.execute(text("TRUNCATE TABLE exchange_requests"))
            db.session.execute(text("TRUNCATE TABLE books"))
            db.session.execute(text("TRUNCATE TABLE users"))
            db.session.commit()
        except Exception as e2:
            print(f"Truncate error: {e2}")
            db.session.rollback()


class TestDataIntegrityProperties:
    """Property-based tests for data integrity and persistence"""
    
    @given(user_data=valid_user_data())
    @settings(max_examples=2, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=2000)
    def test_property_9_user_data_integrity(self, app, user_data):
        """
        Property 9: Data Integrity and Persistence
        For any valid user data, the system should maintain referential integrity 
        and enforce database constraints correctly.
        
        Feature: book-exchange-system, Property 9: Data Integrity and Persistence
        Validates: Requirements 9.2, 9.3, 9.4
        """
        with app.app_context():
            clean_database()
            
            # Create user with valid data
            user = User(
                email=user_data['email'],
                password_hash=user_data['password_hash'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=user_data['role']
            )
            
            db.session.add(user)
            db.session.commit()
            
            # Verify user was created correctly
            saved_user = User.query.filter_by(email=user_data['email']).first()
            assert saved_user is not None
            assert saved_user.email == user_data['email']
            assert saved_user.first_name == user_data['first_name']
            assert saved_user.last_name == user_data['last_name']
            assert saved_user.role == user_data['role']
            assert saved_user.created_at is not None
            assert saved_user.updated_at is not None
            
            # Test unique email constraint
            duplicate_user = User(
                email=user_data['email'],  # Same email
                password_hash='different_hash',
                first_name='Different',
                last_name='Name',
                role='user'
            )
            
            db.session.add(duplicate_user)
            
            # Should raise integrity error due to unique constraint
            with pytest.raises(IntegrityError):
                db.session.commit()
            
            db.session.rollback()
    
    @given(user_data=valid_user_data(), book_data=valid_book_data())
    @settings(max_examples=2, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=2000)
    def test_property_9_book_user_relationship_integrity(self, app, user_data, book_data):
        """
        Property 9: Data Integrity and Persistence
        For any valid user and book data, the system should maintain referential integrity 
        between users and their book listings with proper foreign key constraints.
        
        Feature: book-exchange-system, Property 9: Data Integrity and Persistence
        Validates: Requirements 9.2, 9.3, 9.4
        """
        with app.app_context():
            clean_database()
            
            # Create user first
            user = User(
                email=user_data['email'],
                password_hash=user_data['password_hash'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=user_data['role']
            )
            
            db.session.add(user)
            db.session.commit()
            
            # Create book linked to user
            book = Book(
                user_id=user.id,
                title=book_data['title'],
                author=book_data['author'],
                isbn=book_data.get('isbn'),
                category=book_data['category'],
                condition=book_data['condition'],
                description=book_data.get('description'),
                available=book_data['available']
            )
            
            db.session.add(book)
            db.session.commit()
            
            # Verify book was created with correct relationship
            saved_book = Book.query.filter_by(title=book_data['title']).first()
            assert saved_book is not None
            assert saved_book.user_id == user.id
            assert saved_book.owner == user
            assert saved_book.title == book_data['title']
            assert saved_book.author == book_data['author']
            assert saved_book.category == book_data['category']
            assert saved_book.condition == book_data['condition']
            
            # Verify user has the book in their books relationship
            user_books = user.books
            assert len(user_books) == 1
            assert user_books[0].id == saved_book.id
            
            # Test foreign key constraint - try to create book with invalid user_id
            invalid_book = Book(
                user_id=99999,  # Non-existent user ID
                title='Invalid Book',
                author='Invalid Author',
                category='Fiction',
                condition='good'
            )
            
            db.session.add(invalid_book)
            
            # Should raise integrity error due to foreign key constraint
            with pytest.raises(IntegrityError):
                db.session.commit()
            
            db.session.rollback()
    
    @given(user_data1=valid_user_data(), user_data2=valid_user_data(), book_data=valid_book_data())
    @settings(max_examples=2, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=3000)
    def test_property_9_exchange_request_integrity(self, app, user_data1, user_data2, book_data):
        """
        Property 9: Data Integrity and Persistence
        For any valid exchange request data, the system should maintain relationships 
        between users, books, and exchange requests with proper constraints.
        
        Feature: book-exchange-system, Property 9: Data Integrity and Persistence
        Validates: Requirements 9.2, 9.3, 9.4
        """
        with app.app_context():
            clean_database()
            
            # Ensure different emails for the two users
            if user_data1['email'] == user_data2['email']:
                user_data2['email'] = 'different_' + user_data2['email']
            
            # Create two users
            user1 = User(
                email=user_data1['email'],
                password_hash=user_data1['password_hash'],
                first_name=user_data1['first_name'],
                last_name=user_data1['last_name'],
                role=user_data1['role']
            )
            
            user2 = User(
                email=user_data2['email'],
                password_hash=user_data2['password_hash'],
                first_name=user_data2['first_name'],
                last_name=user_data2['last_name'],
                role=user_data2['role']
            )
            
            db.session.add_all([user1, user2])
            db.session.commit()
            
            # Create book owned by user1
            book = Book(
                user_id=user1.id,
                title=book_data['title'],
                author=book_data['author'],
                isbn=book_data.get('isbn'),
                category=book_data['category'],
                condition=book_data['condition'],
                description=book_data.get('description'),
                available=True
            )
            
            db.session.add(book)
            db.session.commit()
            
            # Create exchange request from user2 to user1 for the book
            exchange_request = ExchangeRequest(
                requester_id=user2.id,
                owner_id=user1.id,
                book_id=book.id,
                status='pending',
                message='I would like to exchange this book'
            )
            
            db.session.add(exchange_request)
            db.session.commit()
            
            # Verify exchange request was created with correct relationships
            saved_request = ExchangeRequest.query.filter_by(
                requester_id=user2.id,
                book_id=book.id
            ).first()
            
            assert saved_request is not None
            assert saved_request.requester_id == user2.id
            assert saved_request.owner_id == user1.id
            assert saved_request.book_id == book.id
            assert saved_request.status == 'pending'
            assert saved_request.requester == user2
            assert saved_request.owner == user1
            assert saved_request.book == book
    
    @given(invalid_data=invalid_user_data())
    @settings(max_examples=2, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_9_user_constraint_validation(self, app, invalid_data):
        """
        Property 9: Data Integrity and Persistence
        For any invalid user data, the system should enforce check constraints 
        and prevent invalid data entry.
        
        Feature: book-exchange-system, Property 9: Data Integrity and Persistence
        Validates: Requirements 9.4
        """
        with app.app_context():
            clean_database()
            
            # Create user with invalid data
            user = User(
                email=invalid_data['email'],
                password_hash=invalid_data['password_hash'],
                first_name=invalid_data['first_name'],
                last_name=invalid_data['last_name'],
                role=invalid_data['role']
            )
            
            db.session.add(user)
            
            # Should raise integrity error due to check constraints
            # Check constraints raise OperationalError, not IntegrityError
            with pytest.raises((IntegrityError, OperationalError)):
                db.session.commit()
            
            db.session.rollback()
    
    @given(user_data=valid_user_data(), invalid_data=invalid_book_data())
    @settings(max_examples=2, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=2000)
    def test_property_9_book_constraint_validation(self, app, user_data, invalid_data):
        """
        Property 9: Data Integrity and Persistence
        For any invalid book data, the system should enforce check constraints 
        and prevent invalid data entry.
        
        Feature: book-exchange-system, Property 9: Data Integrity and Persistence
        Validates: Requirements 9.4
        """
        with app.app_context():
            clean_database()
            
            # Create valid user first
            user = User(
                email=user_data['email'],
                password_hash=user_data['password_hash'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=user_data['role']
            )
            
            db.session.add(user)
            db.session.commit()
            
            # Create book with invalid data
            book = Book(
                user_id=user.id,
                title=invalid_data['title'],
                author=invalid_data['author'],
                category=invalid_data['category'],
                condition=invalid_data['condition'],
                isbn=invalid_data.get('isbn')
            )
            
            db.session.add(book)
            
            # Should raise integrity error due to check constraints
            # Check constraints raise OperationalError, not IntegrityError
            with pytest.raises((IntegrityError, OperationalError)):
                db.session.commit()
            
            db.session.rollback()
    
    @given(user_data=valid_user_data(), book_data=valid_book_data())
    @settings(max_examples=2, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=2000)
    def test_property_9_cascade_delete_integrity(self, app, user_data, book_data):
        """
        Property 9: Data Integrity and Persistence
        For any user deletion, the system should properly handle cascade operations 
        to maintain referential integrity.
        
        Feature: book-exchange-system, Property 9: Data Integrity and Persistence
        Validates: Requirements 9.2, 9.3, 9.4
        """
        with app.app_context():
            clean_database()
            
            # Create user
            user = User(
                email=user_data['email'],
                password_hash=user_data['password_hash'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=user_data['role']
            )
            
            db.session.add(user)
            db.session.commit()
            
            # Create book owned by user
            book = Book(
                user_id=user.id,
                title=book_data['title'],
                author=book_data['author'],
                isbn=book_data.get('isbn'),
                category=book_data['category'],
                condition=book_data['condition'],
                description=book_data.get('description'),
                available=True
            )
            
            db.session.add(book)
            db.session.commit()
            
            # Create user interaction
            interaction = UserInteraction(
                user_id=user.id,
                book_id=book.id,
                interaction_type='view'
            )
            
            db.session.add(interaction)
            db.session.commit()
            
            # Store IDs for verification
            user_id = user.id
            book_id = book.id
            interaction_id = interaction.id
            
            # Verify all records exist
            assert User.query.filter_by(id=user_id).first() is not None
            assert Book.query.filter_by(id=book_id).first() is not None
            assert UserInteraction.query.filter_by(id=interaction_id).first() is not None
            
            # Delete user - should cascade delete related records
            # First, we need to expunge the objects from the session to avoid issues
            db.session.expunge(user)
            db.session.expunge(book)
            db.session.expunge(interaction)
            
            # Get fresh instances and delete
            user_to_delete = User.query.filter_by(id=user_id).first()
            db.session.delete(user_to_delete)
            db.session.commit()
            
            # Verify cascade deletion worked
            assert User.query.filter_by(id=user_id).first() is None
            assert Book.query.filter_by(id=book_id).first() is None
            assert UserInteraction.query.filter_by(id=interaction_id).first() is None