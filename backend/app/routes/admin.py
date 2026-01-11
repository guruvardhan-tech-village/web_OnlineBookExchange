from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, desc
from datetime import datetime, timedelta

from ..models.user import User
from ..models.book import Book
from ..models.exchange_request import ExchangeRequest
from ..models.user_interaction import UserInteraction
from ..utils.auth import admin_required
from ..utils.responses import success_response, error_response
from .. import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
@admin_required
def get_stats():
    """Get system statistics for admin dashboard"""
    try:
        # Basic counts
        total_users = User.query.count()
        total_books = Book.query.count()
        total_exchanges = ExchangeRequest.query.count()
        
        # Active statistics
        active_books = Book.query.filter_by(available=True).count()
        pending_exchanges = ExchangeRequest.query.filter_by(status='pending').count()
        completed_exchanges = ExchangeRequest.query.filter_by(status='completed').count()
        
        # Recent activity (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        new_users_month = User.query.filter(User.created_at >= thirty_days_ago).count()
        new_books_month = Book.query.filter(Book.created_at >= thirty_days_ago).count()
        new_exchanges_month = ExchangeRequest.query.filter(ExchangeRequest.created_at >= thirty_days_ago).count()
        
        # Popular categories
        popular_categories = db.session.query(
            Book.category,
            func.count(Book.id).label('count')
        ).group_by(Book.category).order_by(desc('count')).limit(5).all()
        
        # Top users by book count
        top_users = db.session.query(
            User.first_name,
            User.last_name,
            User.email,
            func.count(Book.id).label('book_count')
        ).join(Book).group_by(User.id).order_by(desc('book_count')).limit(5).all()
        
        # Exchange success rate
        total_non_pending = ExchangeRequest.query.filter(ExchangeRequest.status != 'pending').count()
        success_rate = (completed_exchanges / total_non_pending * 100) if total_non_pending > 0 else 0
        
        stats = {
            'overview': {
                'total_users': total_users,
                'total_books': total_books,
                'total_exchanges': total_exchanges,
                'active_books': active_books,
                'pending_exchanges': pending_exchanges,
                'completed_exchanges': completed_exchanges,
                'exchange_success_rate': round(success_rate, 2)
            },
            'recent_activity': {
                'new_users_month': new_users_month,
                'new_books_month': new_books_month,
                'new_exchanges_month': new_exchanges_month
            },
            'popular_categories': [
                {'category': cat, 'count': count} 
                for cat, count in popular_categories
            ],
            'top_users': [
                {
                    'name': f"{first_name} {last_name}",
                    'email': email,
                    'book_count': book_count
                }
                for first_name, last_name, email, book_count in top_users
            ]
        }
        
        return success_response(stats, 'System statistics retrieved successfully')
        
    except Exception as e:
        return error_response(f'Failed to retrieve statistics: {str(e)}', 500)

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    """Get all users for admin management with pagination and search"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        search = request.args.get('search', '').strip()
        role_filter = request.args.get('role', '').strip()
        
        # Build query
        query = User.query
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                db.or_(
                    User.first_name.ilike(search_term),
                    User.last_name.ilike(search_term),
                    User.email.ilike(search_term)
                )
            )
        
        # Apply role filter
        if role_filter and role_filter in ['user', 'admin']:
            query = query.filter(User.role == role_filter)
        
        # Order by creation date (newest first)
        query = query.order_by(desc(User.created_at))
        
        # Paginate
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        users_data = []
        for user in pagination.items:
            user_dict = user.to_dict()
            # Add additional stats
            user_dict['book_count'] = Book.query.filter_by(user_id=user.id).count()
            user_dict['exchange_count'] = ExchangeRequest.query.filter(
                db.or_(
                    ExchangeRequest.requester_id == user.id,
                    ExchangeRequest.owner_id == user.id
                )
            ).count()
            users_data.append(user_dict)
        
        response_data = {
            'users': users_data,
            'pagination': {
                'page': pagination.page,
                'pages': pagination.pages,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }
        
        return success_response(response_data, 'Users retrieved successfully')
        
    except Exception as e:
        return error_response(f'Failed to retrieve users: {str(e)}', 500)

@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@jwt_required()
@admin_required
def update_user_role(user_id):
    """Update user role (promote/demote)"""
    try:
        data = request.get_json()
        if not data or 'role' not in data:
            return error_response('Role is required', 400)
        
        new_role = data['role'].strip().lower()
        if new_role not in ['user', 'admin']:
            return error_response('Invalid role. Must be "user" or "admin"', 400)
        
        # Find user
        user = User.query.get(user_id)
        if not user:
            return error_response('User not found', 404)
        
        # Prevent self-demotion
        current_user_id = int(get_jwt_identity())
        if user_id == current_user_id and new_role == 'user':
            return error_response('Cannot demote yourself', 400)
        
        # Update role
        old_role = user.role
        user.role = new_role
        user.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return success_response(
            user.to_dict(),
            f'User role updated from {old_role} to {new_role}'
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to update user role: {str(e)}', 500)

@admin_bp.route('/books/pending', methods=['GET'])
@jwt_required()
@admin_required
def get_pending_books():
    """Get books that need moderation (for future moderation workflow)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
        # For now, return recently added books that might need review
        # In a full implementation, you'd have a 'moderation_status' field
        query = Book.query.order_by(desc(Book.created_at))
        
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        books_data = []
        for book in pagination.items:
            book_dict = book.to_dict()
            # Add moderation-relevant info
            book_dict['exchange_requests_count'] = ExchangeRequest.query.filter_by(book_id=book.id).count()
            book_dict['interactions_count'] = UserInteraction.query.filter_by(book_id=book.id).count()
            books_data.append(book_dict)
        
        response_data = {
            'books': books_data,
            'pagination': {
                'page': pagination.page,
                'pages': pagination.pages,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }
        
        return success_response(response_data, 'Books retrieved successfully')
        
    except Exception as e:
        return error_response(f'Failed to retrieve books: {str(e)}', 500)

@admin_bp.route('/books/<int:book_id>/moderate', methods=['PUT'])
@jwt_required()
@admin_required
def moderate_book(book_id):
    """Moderate book listing (approve/reject/remove)"""
    try:
        data = request.get_json()
        if not data or 'action' not in data:
            return error_response('Action is required', 400)
        
        action = data['action'].strip().lower()
        reason = data.get('reason', '').strip()
        
        if action not in ['approve', 'reject', 'remove']:
            return error_response('Invalid action. Must be "approve", "reject", or "remove"', 400)
        
        # Find book
        book = Book.query.get(book_id)
        if not book:
            return error_response('Book not found', 404)
        
        if action == 'remove':
            # Remove book and cascade to related records
            db.session.delete(book)
            message = f'Book "{book.title}" has been removed'
        elif action == 'reject':
            # Mark as unavailable (soft rejection)
            book.available = False
            book.updated_at = datetime.utcnow()
            message = f'Book "{book.title}" has been rejected'
        else:  # approve
            # Ensure book is available
            book.available = True
            book.updated_at = datetime.utcnow()
            message = f'Book "{book.title}" has been approved'
        
        db.session.commit()
        
        # Log moderation action (in a full system, you'd have a moderation log table)
        current_user_id = int(get_jwt_identity())
        
        response_data = {
            'book_id': book_id,
            'action': action,
            'reason': reason,
            'moderated_by': current_user_id,
            'moderated_at': datetime.utcnow().isoformat()
        }
        
        return success_response(response_data, message)
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to moderate book: {str(e)}', 500)