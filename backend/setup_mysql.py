#!/usr/bin/env python3
"""
MySQL Database Setup Script
Creates databases and tables for the Book Exchange System
"""

import pymysql
import sys
import os
from app import create_app, db

def create_databases():
    """Create the main and test databases if they don't exist"""
    try:
        # Connect to MySQL server (without specifying database)
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='Soma@9985'
        )
        
        cursor = connection.cursor()
        
        # Create main database
        cursor.execute("CREATE DATABASE IF NOT EXISTS MajorProject CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✓ Created/verified main database: MajorProject")
        
        # Create test database
        cursor.execute("CREATE DATABASE IF NOT EXISTS MajorProject_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✓ Created/verified test database: MajorProject_test")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating databases: {e}")
        return False

def test_connection():
    """Test the database connection"""
    try:
        app = create_app('development')
        
        with app.app_context():
            # Test basic database operations
            from sqlalchemy import text
            result = db.session.execute(text("SELECT 1 as test")).fetchone()
            if result and result[0] == 1:
                print("✓ Database connection test successful")
                return True
            else:
                print("✗ Database connection test failed")
                return False
                
    except Exception as e:
        print(f"✗ Database connection error: {e}")
        return False

def create_tables():
    """Create all tables using SQLAlchemy"""
    try:
        app = create_app('development')
        
        with app.app_context():
            # Import models to ensure they're registered
            from app.models.user import User
            from app.models.book import Book
            from app.models.exchange_request import ExchangeRequest
            from app.models.user_interaction import UserInteraction
            
            # Drop all tables and recreate (for clean setup)
            print("Creating database tables...")
            db.create_all()
            print("✓ All tables created successfully")
            
            # Verify tables were created
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"✓ Created tables: {', '.join(tables)}")
            
        return True
        
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        return False

def main():
    """Main setup function"""
    print("=== MySQL Database Setup for Book Exchange System ===\n")
    
    # Step 1: Create databases
    print("Step 1: Creating databases...")
    if not create_databases():
        print("Failed to create databases. Exiting.")
        sys.exit(1)
    
    # Step 2: Test connection
    print("\nStep 2: Testing database connection...")
    if not test_connection():
        print("Failed to connect to database. Exiting.")
        sys.exit(1)
    
    # Step 3: Create tables
    print("\nStep 3: Creating database tables...")
    if not create_tables():
        print("Failed to create tables. Exiting.")
        sys.exit(1)
    
    print("\n=== Database setup completed successfully! ===")
    print("\nNext steps:")
    print("1. Run tests: python -m pytest tests/ -v")
    print("2. Start the application: python run.py")
    print("3. Seed sample data: python seed_data.py")

if __name__ == '__main__':
    main()