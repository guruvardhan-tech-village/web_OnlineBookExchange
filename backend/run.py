#!/usr/bin/env python3
"""
Application entry point
"""
import os
import pymysql
from dotenv import load_dotenv
from app import create_app, db

# Use PyMySQL as MySQL driver
pymysql.install_as_MySQLdb()

# Load environment variables
load_dotenv()

app = create_app()

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print("Database initialized!")

@app.cli.command()
def seed_db():
    """Seed the database with sample data"""
    from app.models.user import User
    from app.models.book import Book
    from werkzeug.security import generate_password_hash
    
    # Create admin user
    admin = User(
        email='admin@bookexchange.com',
        password_hash=generate_password_hash('admin123'),
        first_name='Admin',
        last_name='User',
        role='admin'
    )
    
    # Create regular user
    user = User(
        email='user@bookexchange.com',
        password_hash=generate_password_hash('user123'),
        first_name='John',
        last_name='Doe',
        role='user'
    )
    
    db.session.add(admin)
    db.session.add(user)
    db.session.commit()
    
    # Create sample books
    book1 = Book(
        user_id=user.id,
        title='The Great Gatsby',
        author='F. Scott Fitzgerald',
        isbn='9780743273565',
        category='Fiction',
        condition='good',
        description='Classic American novel about the Jazz Age'
    )
    
    book2 = Book(
        user_id=user.id,
        title='To Kill a Mockingbird',
        author='Harper Lee',
        isbn='9780061120084',
        category='Fiction',
        condition='like_new',
        description='Pulitzer Prize-winning novel about racial injustice'
    )
    
    db.session.add(book1)
    db.session.add(book2)
    db.session.commit()
    
    print("Database seeded with sample data!")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)