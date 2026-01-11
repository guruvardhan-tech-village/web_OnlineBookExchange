"""
Seed data script for development and testing
"""
from app import create_app, db
from app.models.user import User
from app.models.book import Book
from app.models.exchange_request import ExchangeRequest
from app.models.user_interaction import UserInteraction
import bcrypt

def seed_database():
    """Populate database with sample data"""
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.session.query(UserInteraction).delete()
        db.session.query(ExchangeRequest).delete()
        db.session.query(Book).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        # Create users
        print("Creating users...")
        password_hash = bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        admin_user = User(
            email='admin@bookexchange.com',
            password_hash=password_hash,
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        
        user1 = User(
            email='john.doe@example.com',
            password_hash=password_hash,
            first_name='John',
            last_name='Doe',
            role='user'
        )
        
        user2 = User(
            email='jane.smith@example.com',
            password_hash=password_hash,
            first_name='Jane',
            last_name='Smith',
            role='user'
        )
        
        user3 = User(
            email='bob.wilson@example.com',
            password_hash=password_hash,
            first_name='Bob',
            last_name='Wilson',
            role='user'
        )
        
        db.session.add_all([admin_user, user1, user2, user3])
        db.session.commit()
        
        # Create books
        print("Creating books...")
        books = [
            Book(
                user_id=user1.id,
                title='The Great Gatsby',
                author='F. Scott Fitzgerald',
                isbn='9780743273565',
                category='Fiction',
                condition='good',
                description='A classic American novel set in the Jazz Age',
                available=True
            ),
            Book(
                user_id=user1.id,
                title='To Kill a Mockingbird',
                author='Harper Lee',
                isbn='9780061120084',
                category='Fiction',
                condition='like_new',
                description='A gripping tale of racial injustice and childhood innocence',
                available=True
            ),
            Book(
                user_id=user2.id,
                title='1984',
                author='George Orwell',
                isbn='9780451524935',
                category='Science Fiction',
                condition='good',
                description='A dystopian social science fiction novel',
                available=True
            ),
            Book(
                user_id=user2.id,
                title='Pride and Prejudice',
                author='Jane Austen',
                isbn='9780141439518',
                category='Romance',
                condition='fair',
                description='A romantic novel of manners',
                available=True
            ),
            Book(
                user_id=user3.id,
                title='The Hobbit',
                author='J.R.R. Tolkien',
                isbn='9780547928227',
                category='Fantasy',
                condition='new',
                description='A fantasy novel and children\'s book',
                available=True
            ),
            Book(
                user_id=user3.id,
                title='Harry Potter and the Sorcerer\'s Stone',
                author='J.K. Rowling',
                isbn='9780590353427',
                category='Fantasy',
                condition='good',
                description='The first novel in the Harry Potter series',
                available=False
            ),
        ]
        
        db.session.add_all(books)
        db.session.commit()
        
        # Create exchange requests
        print("Creating exchange requests...")
        exchange1 = ExchangeRequest(
            requester_id=user2.id,
            owner_id=user1.id,
            book_id=books[0].id,
            status='pending',
            message='I would love to read this classic!'
        )
        
        exchange2 = ExchangeRequest(
            requester_id=user3.id,
            owner_id=user2.id,
            book_id=books[2].id,
            status='approved',
            message='This sounds fascinating!'
        )
        
        exchange3 = ExchangeRequest(
            requester_id=user1.id,
            owner_id=user3.id,
            book_id=books[5].id,
            status='completed',
            message='My kids would love this book!'
        )
        
        db.session.add_all([exchange1, exchange2, exchange3])
        db.session.commit()
        
        # Create user interactions
        print("Creating user interactions...")
        interactions = [
            UserInteraction(user_id=user1.id, book_id=books[2].id, interaction_type='view'),
            UserInteraction(user_id=user1.id, book_id=books[3].id, interaction_type='view'),
            UserInteraction(user_id=user1.id, book_id=books[4].id, interaction_type='like'),
            UserInteraction(user_id=user2.id, book_id=books[0].id, interaction_type='view'),
            UserInteraction(user_id=user2.id, book_id=books[0].id, interaction_type='request'),
            UserInteraction(user_id=user3.id, book_id=books[1].id, interaction_type='view'),
            UserInteraction(user_id=user3.id, book_id=books[2].id, interaction_type='like'),
        ]
        
        db.session.add_all(interactions)
        db.session.commit()
        
        print("\nSeed data created successfully!")
        print(f"Created {User.query.count()} users")
        print(f"Created {Book.query.count()} books")
        print(f"Created {ExchangeRequest.query.count()} exchange requests")
        print(f"Created {UserInteraction.query.count()} user interactions")
        print("\nDefault login credentials:")
        print("Admin: admin@bookexchange.com / password123")
        print("User 1: john.doe@example.com / password123")
        print("User 2: jane.smith@example.com / password123")
        print("User 3: bob.wilson@example.com / password123")

if __name__ == '__main__':
    seed_database()
