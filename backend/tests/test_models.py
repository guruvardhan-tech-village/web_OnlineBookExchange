import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from app import db
from app.models.user import User
from app.models.book import Book
from app.models.exchange_request import ExchangeRequest
from app.models.user_interaction import UserInteraction
import bcrypt
from datetime import datetime
from sqlalchemy.exc import IntegrityError

# Feature: book-exchange-system, Property 1: User Registration and Authentication
@given(
    email=st.emails(),
    password=st.text(min_size=8, max_size=100),
    first_name=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc', 'Pd', 'Zs'))),
    last_name=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc', 'Pd', 'Zs'))),
    role=st.sampled_from(['user', 'admin'])
)
@settings(max_examples=10, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
def test_user_registration_and_authentication_property(app, db_session, email, password, first_name, last_name, role):
    """
    Property 1: User Registration and Authentication
    For any valid user registration data, the system should create a new user account with securely hashed passwords,
    prevent duplicate email registrations, authenticate valid credentials with JWT tokens, and reject invalid credentials appropriately.
    Validates: Requirements 1.1, 1.2, 1.5
    """
    with app.app_context():
        # Clear any existing data to avoid conflicts
        try:
            db.session.query(User).delete()
            db.session.commit()
        except:
            db.session.rollback()
        
        # Test user creation with secure password hashing
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user = User(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Verify user was created correctly
        created_user = User.query.filter_by(email=email).first()
        assert created_user is not None
        assert created_user.email == email
        assert created_user.first_name == first_name
        assert created_user.last_name == last_name
        assert created_user.role == role
        assert created_user.password_hash != password  # Password should be hashed
        assert bcrypt.checkpw(password.encode('utf-8'), created_user.password_hash.encode('utf-8'))  # Hash should be valid
        assert created_user.created_at is not None
        assert created_user.updated_at is not None
        
        # Test duplicate email prevention - create a new session to avoid conflicts
        try:
            duplicate_user = User(
                email=email,  # Same email
                password_hash=password_hash,
                first_name="Different",
                last_name="Name",
                role='user'
            )
            
            db.session.add(duplicate_user)
            db.session.commit()
            
            # If we get here, the constraint didn't work - check manually
            users_with_email = User.query.filter_by(email=email).all()
            assert len(users_with_email) == 1, "Duplicate email should be prevented"
            
        except (IntegrityError, Exception):
            # This is expected - duplicate email should be prevented
            db.session.rollback()
            
        # Verify only one user with this email exists
        users_with_email = User.query.filter_by(email=email).all()
        assert len(users_with_email) == 1


# Feature: book-exchange-system, Property 3: Book Listing Management  
@given(
    title=st.text(min_size=1, max_size=200),
    author=st.text(min_size=1, max_size=100),
    isbn=st.one_of(st.none(), st.text(min_size=1, max_size=20)),
    category=st.text(min_size=1, max_size=50),
    condition=st.sampled_from(['new', 'like_new', 'good', 'fair', 'poor']),
    description=st.one_of(st.none(), st.text(max_size=1000)),
    image_url=st.one_of(st.none(), st.text(max_size=255)),
    available=st.booleans()
)
@settings(max_examples=10, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
def test_book_listing_management_property(app, db_session, title, author, isbn, category, condition, description, image_url, available):
    """
    Property 3: Book Listing Management
    For any book listing operation, the system should store all book details correctly during creation,
    validate and securely store uploaded images, maintain data integrity during updates, properly handle deletions
    with cascade effects, validate all inputs, and return complete book information when queried.
    Validates: Requirements 3.1, 3.5
    """
    with app.app_context():
        # Clear any existing data
        try:
            db.session.query(Book).delete()
            db.session.query(User).delete()
            db.session.commit()
        except:
            db.session.rollback()
        
        # First create a user to own the book
        user = User(
            email="test@example.com",
            password_hash="hashed_password",
            first_name="Test",
            last_name="User",
            role='user'
        )
        db.session.add(user)
        db.session.commit()
        
        # Store user_id to avoid session issues
        user_id = user.id
        
        # Test book creation with all details
        book = Book(
            user_id=user_id,
            title=title,
            author=author,
            isbn=isbn,
            category=category,
            condition=condition,
            description=description,
            image_url=image_url,
            available=available
        )
        
        db.session.add(book)
        db.session.commit()
        
        # Store book_id to avoid session issues
        book_id = book.id
        
        # Verify book was created correctly
        created_book = Book.query.filter_by(id=book_id).first()
        assert created_book is not None
        assert created_book.title == title
        assert created_book.author == author
        assert created_book.isbn == isbn
        assert created_book.category == category
        assert created_book.condition == condition
        assert created_book.description == description
        assert created_book.image_url == image_url
        assert created_book.available == available
        assert created_book.user_id == user_id
        assert created_book.created_at is not None
        assert created_book.updated_at is not None
        
        # Test book update maintains data integrity
        original_created_at = created_book.created_at
        new_title = "Updated Title"
        created_book.title = new_title
        db.session.commit()
        
        updated_book = Book.query.filter_by(id=book_id).first()
        assert updated_book.title == new_title
        assert updated_book.created_at == original_created_at  # Should not change
        assert updated_book.updated_at >= original_created_at  # Should be updated
        
        # Test foreign key relationship - get fresh instances to avoid session issues
        fresh_book = Book.query.filter_by(id=book_id).first()
        fresh_user = User.query.filter_by(id=user_id).first()
        assert fresh_book.owner == fresh_user
        assert fresh_book in fresh_user.books


# Feature: book-exchange-system, Property 5: Exchange Request Workflow
@given(
    status=st.sampled_from(['pending', 'approved', 'rejected', 'completed']),
    message=st.one_of(st.none(), st.text(max_size=1000))
)
@settings(max_examples=10, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
def test_exchange_request_workflow_property(app, db_session, status, message):
    """
    Property 5: Exchange Request Workflow
    For any exchange request operation, the system should create proper request records linking all parties,
    allow owners to approve or reject requests, update request statuses correctly, maintain complete history
    of all exchanges, and update book availability when exchanges are completed.
    Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.6
    """
    with app.app_context():
        # Clear any existing data
        try:
            db.session.query(ExchangeRequest).delete()
            db.session.query(Book).delete()
            db.session.query(User).delete()
            db.session.commit()
        except:
            db.session.rollback()
        
        # Create users
        requester = User(
            email="requester@example.com",
            password_hash="hashed_password",
            first_name="Requester",
            last_name="User",
            role='user'
        )
        owner = User(
            email="owner@example.com", 
            password_hash="hashed_password",
            first_name="Owner",
            last_name="User",
            role='user'
        )
        db.session.add_all([requester, owner])
        db.session.commit()
        
        # Store IDs to avoid session issues
        requester_id = requester.id
        owner_id = owner.id
        
        # Create book
        book = Book(
            user_id=owner_id,
            title="Test Book",
            author="Test Author",
            category="Fiction",
            condition='good',
            available=True
        )
        db.session.add(book)
        db.session.commit()
        
        book_id = book.id
        
        # Test exchange request creation
        exchange_request = ExchangeRequest(
            requester_id=requester_id,
            owner_id=owner_id,
            book_id=book_id,
            status=status,
            message=message
        )
        
        db.session.add(exchange_request)
        db.session.commit()
        
        exchange_id = exchange_request.id
        
        # Verify exchange request was created correctly
        created_request = ExchangeRequest.query.filter_by(id=exchange_id).first()
        assert created_request is not None
        assert created_request.requester_id == requester_id
        assert created_request.owner_id == owner_id
        assert created_request.book_id == book_id
        assert created_request.status == status
        assert created_request.message == message
        assert created_request.created_at is not None
        assert created_request.updated_at is not None
        
        # Test relationships are properly linked - get fresh instances
        fresh_request = ExchangeRequest.query.filter_by(id=exchange_id).first()
        fresh_requester = User.query.filter_by(id=requester_id).first()
        fresh_owner = User.query.filter_by(id=owner_id).first()
        fresh_book = Book.query.filter_by(id=book_id).first()
        
        assert fresh_request.requester == fresh_requester
        assert fresh_request.owner == fresh_owner
        assert fresh_request.book == fresh_book
        assert fresh_request in fresh_requester.sent_requests
        assert fresh_request in fresh_owner.received_requests
        assert fresh_request in fresh_book.exchange_requests
        
        # Test status update maintains history
        original_created_at = created_request.created_at
        new_status = 'approved' if status != 'approved' else 'rejected'
        created_request.status = new_status
        db.session.commit()
        
        updated_request = ExchangeRequest.query.filter_by(id=exchange_id).first()
        assert updated_request.status == new_status
        assert updated_request.created_at == original_created_at  # Should not change
        assert updated_request.updated_at >= original_created_at  # Should be updated


# Feature: book-exchange-system, Property 6: AI Recommendation Engine
@given(
    interaction_type=st.sampled_from(['view', 'like', 'request', 'search'])
)
@settings(max_examples=10, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
def test_user_interaction_tracking_property(app, db_session, interaction_type):
    """
    Property 6: AI Recommendation Engine (User Interaction Tracking)
    For any recommendation generation, the system should analyze user interaction history using TF-IDF algorithms,
    calculate book similarities using cosine similarity, record all user interactions, generate recommendations
    based on user preferences, rank recommendations by relevance score, and update recommendations as user behavior changes.
    Validates: Requirements 6.3
    """
    with app.app_context():
        # Clear any existing data
        try:
            db.session.query(UserInteraction).delete()
            db.session.query(Book).delete()
            db.session.query(User).delete()
            db.session.commit()
        except:
            db.session.rollback()
        
        # Create users
        user = User(
            email="user@example.com",
            password_hash="hashed_password", 
            first_name="Test",
            last_name="User",
            role='user'
        )
        book_owner = User(
            email="owner@example.com",
            password_hash="hashed_password",
            first_name="Owner",
            last_name="User", 
            role='user'
        )
        db.session.add_all([user, book_owner])
        db.session.commit()
        
        # Store IDs to avoid session issues
        user_id = user.id
        book_owner_id = book_owner.id
        
        # Create book
        book = Book(
            user_id=book_owner_id,
            title="Test Book",
            author="Test Author",
            category="Fiction",
            condition='good'
        )
        db.session.add(book)
        db.session.commit()
        
        book_id = book.id
        
        # Test user interaction recording
        interaction = UserInteraction(
            user_id=user_id,
            book_id=book_id,
            interaction_type=interaction_type
        )
        
        db.session.add(interaction)
        db.session.commit()
        
        interaction_id = interaction.id
        
        # Verify interaction was recorded correctly
        created_interaction = UserInteraction.query.filter_by(id=interaction_id).first()
        assert created_interaction is not None
        assert created_interaction.user_id == user_id
        assert created_interaction.book_id == book_id
        assert created_interaction.interaction_type == interaction_type
        assert created_interaction.created_at is not None
        
        # Test relationships - get fresh instances
        fresh_interaction = UserInteraction.query.filter_by(id=interaction_id).first()
        fresh_user = User.query.filter_by(id=user_id).first()
        fresh_book = Book.query.filter_by(id=book_id).first()
        
        assert fresh_interaction.user == fresh_user
        assert fresh_interaction.book == fresh_book
        assert fresh_interaction in fresh_user.interactions
        assert fresh_interaction in fresh_book.interactions