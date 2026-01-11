import pytest
import os
from app import create_app, db
from app.models.user import User
from app.models.book import Book
from app.models.exchange_request import ExchangeRequest
from app.models.user_interaction import UserInteraction
from sqlalchemy import text

@pytest.fixture(scope='function')
def app():
    """Create application for testing"""
    # Clear any existing environment variables that might interfere
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']
    
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://root:Soma%409985@localhost:3306/MajorProject_test',
        'WTF_CSRF_ENABLED': False,
        'JWT_ACCESS_TOKEN_EXPIRES': False,
        'SECRET_KEY': 'test-secret-key',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    
    with app.app_context():
        # Ensure database exists
        try:
            # Create database if it doesn't exist
            from sqlalchemy import create_engine
            engine = create_engine('mysql+pymysql://root:Soma%409985@localhost:3306/')
            with engine.connect() as conn:
                conn.execute(text("CREATE DATABASE IF NOT EXISTS MajorProject_test"))
                conn.commit()
        except Exception as e:
            print(f"Database creation error: {e}")
        
        # Clean up any existing data and recreate tables
        try:
            # Drop all tables first
            db.drop_all()
        except Exception as e:
            print(f"Drop tables error: {e}")
        
        try:
            # Create all tables
            db.create_all()
            # Verify tables were created
            result = db.session.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            print(f"Created tables: {tables}")
        except Exception as e:
            print(f"Create tables error: {e}")
            raise
        
        yield app
        
        # Clean up after test
        try:
            db.session.remove()
        except Exception:
            pass

@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture(scope='function')
def db_session(app):
    """Create database session for testing"""
    with app.app_context():
        yield db.session
        try:
            db.session.rollback()
        except Exception:
            pass