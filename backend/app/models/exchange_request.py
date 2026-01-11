from .. import db
from datetime import datetime

class ExchangeRequest(db.Model):
    """Exchange request model for book trading"""
    __tablename__ = 'exchange_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False, index=True)
    status = db.Column(db.Enum('pending', 'approved', 'rejected', 'completed', name='exchange_statuses'), 
                      default='pending', nullable=False, index=True)
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Enhanced constraints and indexes
    __table_args__ = (
        db.CheckConstraint('requester_id != owner_id', name='different_users_check'),
        db.UniqueConstraint('requester_id', 'book_id', 'status', name='unique_active_request'),
        db.Index('idx_exchange_requester_status', 'requester_id', 'status'),
        db.Index('idx_exchange_owner_status', 'owner_id', 'status'),
        db.Index('idx_exchange_book_status', 'book_id', 'status'),
        db.Index('idx_exchange_status_created', 'status', 'created_at'),
        db.Index('idx_exchange_users_book', 'requester_id', 'owner_id', 'book_id'),
    )
    
    def __repr__(self):
        return f'<ExchangeRequest {self.id}: {self.status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'requester_id': self.requester_id,
            'owner_id': self.owner_id,
            'book_id': self.book_id,
            'status': self.status,
            'message': self.message,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'requester': self.requester.to_dict() if self.requester else None,
            'owner': self.owner.to_dict() if self.owner else None,
            'book': self.book.to_dict() if self.book else None
        }