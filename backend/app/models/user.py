from .. import db
from datetime import datetime

class User(db.Model):
    """User model for authentication and profile management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Enum('user', 'admin', name='user_roles'), default='user', nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Additional constraints and indexes
    __table_args__ = (
        db.CheckConstraint("email LIKE '%@%'", name='valid_email_check'),
        db.CheckConstraint("LENGTH(first_name) >= 1", name='first_name_not_empty'),
        db.CheckConstraint("LENGTH(last_name) >= 1", name='last_name_not_empty'),
        db.Index('idx_user_role_created', 'role', 'created_at'),
        db.Index('idx_user_name_search', 'first_name', 'last_name'),
    )
    
    # Relationships
    books = db.relationship('Book', backref='owner', lazy=True, cascade='all, delete-orphan')
    sent_requests = db.relationship('ExchangeRequest', 
                                  foreign_keys='ExchangeRequest.requester_id', 
                                  backref='requester', 
                                  lazy=True)
    received_requests = db.relationship('ExchangeRequest', 
                                      foreign_keys='ExchangeRequest.owner_id', 
                                      backref='owner', 
                                      lazy=True)
    interactions = db.relationship('UserInteraction', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }