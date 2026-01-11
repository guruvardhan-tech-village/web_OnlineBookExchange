#!/usr/bin/env python3
"""
Database initialization script
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db

def init_database():
    """Initialize the database with tables"""
    app = create_app()
    
    with app.app_context():
        # Import all models to ensure they're registered
        from app.models.user import User
        from app.models.book import Book
        from app.models.exchange_request import ExchangeRequest
        from app.models.user_interaction import UserInteraction
        
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Create uploads directory
        uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads', 'books')
        os.makedirs(uploads_dir, exist_ok=True)
        print("Upload directories created successfully!")

if __name__ == '__main__':
    init_database()