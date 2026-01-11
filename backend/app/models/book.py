from .. import db
from datetime import datetime

class Book(db.Model):
    """Book model for book listings"""
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    author = db.Column(db.String(100), nullable=False, index=True)
    isbn = db.Column(db.String(20), nullable=True, unique=True)
    category = db.Column(db.String(50), nullable=False, index=True)
    condition = db.Column(db.Enum('new', 'like_new', 'good', 'fair', 'poor', name='book_conditions'), 
                         nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    available = db.Column(db.Boolean, default=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Additional constraints and indexes for search performance
    __table_args__ = (
        db.CheckConstraint("LENGTH(title) >= 1", name='title_not_empty'),
        db.CheckConstraint("LENGTH(author) >= 1", name='author_not_empty'),
        db.CheckConstraint("LENGTH(category) >= 1", name='category_not_empty'),
        db.CheckConstraint("isbn IS NULL OR LENGTH(isbn) >= 10", name='valid_isbn_length'),
        db.Index('idx_book_search_main', 'title', 'author', 'category'),
        db.Index('idx_book_available_category', 'available', 'category'),
        db.Index('idx_book_condition_available', 'condition', 'available'),
        db.Index('idx_book_owner_available', 'user_id', 'available'),
        db.Index('idx_book_created_available', 'created_at', 'available'),
        # Full-text search index for title and description
        db.Index('idx_book_text_search', db.text('title, description'), mysql_prefix='FULLTEXT'),
    )
    
    # Relationships
    exchange_requests = db.relationship('ExchangeRequest', backref='book', lazy=True)
    interactions = db.relationship('UserInteraction', backref='book', lazy=True)
    
    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'category': self.category,
            'condition': self.condition,
            'description': self.description,
            'image_url': self.image_url,
            'available': self.available,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'owner': self.owner.to_dict() if self.owner else None
        }