from .. import db
from datetime import datetime

class UserInteraction(db.Model):
    """User interaction model for recommendation tracking"""
    __tablename__ = 'user_interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False, index=True)
    interaction_type = db.Column(db.Enum('view', 'like', 'request', 'search', name='interaction_types'), 
                                nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Enhanced indexes for performance and analytics
    __table_args__ = (
        db.Index('idx_user_interactions', 'user_id', 'created_at'),
        db.Index('idx_book_interactions', 'book_id', 'interaction_type'),
        db.Index('idx_interaction_type_time', 'interaction_type', 'created_at'),
        db.Index('idx_user_book_interaction', 'user_id', 'book_id', 'interaction_type'),
        db.Index('idx_recent_interactions', 'created_at', 'user_id', 'interaction_type'),
        # Composite index for recommendation queries
        db.Index('idx_recommendation_query', 'user_id', 'interaction_type', 'created_at'),
    )
    
    def __repr__(self):
        return f'<UserInteraction {self.user_id}:{self.book_id}:{self.interaction_type}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'interaction_type': self.interaction_type,
            'created_at': self.created_at.isoformat()
        }