from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app import db
from app.models.exchange_request import ExchangeRequest
from app.models.book import Book
from app.schemas.exchange import exchange_create_schema, exchange_update_schema

exchanges_bp = Blueprint('exchanges', __name__)

@exchanges_bp.route('', methods=['GET'])
@jwt_required()
def get_exchanges():
    """Get user's exchange requests"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get query parameters
        status = request.args.get('status')
        type_filter = request.args.get('type')  # 'sent' or 'received'
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        # Build base query
        if type_filter == 'sent':
            query = ExchangeRequest.query.filter_by(requester_id=current_user_id)
        elif type_filter == 'received':
            query = ExchangeRequest.query.filter_by(owner_id=current_user_id)
        else:
            # Get both sent and received
            query = ExchangeRequest.query.filter(
                db.or_(
                    ExchangeRequest.requester_id == current_user_id,
                    ExchangeRequest.owner_id == current_user_id
                )
            )
        
        # Apply status filter if provided
        if status:
            query = query.filter(ExchangeRequest.status == status)
        
        # Order by creation date (newest first)
        query = query.order_by(ExchangeRequest.created_at.desc())
        
        # Paginate results
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        exchanges = [exchange.to_dict() for exchange in pagination.items]
        
        return jsonify({
            'exchanges': exchanges,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Failed to retrieve exchanges'
        }), 500

@exchanges_bp.route('', methods=['POST'])
@jwt_required()
def create_exchange():
    """Create new exchange request"""
    try:
        current_user_id = get_jwt_identity()
        
        # Validate input data
        data = exchange_create_schema.load(request.json)
        book_id = data['book_id']
        message = data.get('message')
        
        # Get the book
        book = Book.query.get(book_id)
        if not book:
            return jsonify({
                'error': 'Not Found',
                'message': 'Book not found'
            }), 404
        
        # Check if book is available
        if not book.available:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Book is not available for exchange'
            }), 400
        
        # Prevent users from requesting their own books
        if book.user_id == current_user_id:
            return jsonify({
                'error': 'Bad Request',
                'message': 'You cannot request your own book'
            }), 400
        
        # Check for duplicate pending requests
        existing_request = ExchangeRequest.query.filter_by(
            requester_id=current_user_id,
            book_id=book_id,
            status='pending'
        ).first()
        
        if existing_request:
            return jsonify({
                'error': 'Conflict',
                'message': 'You already have a pending request for this book'
            }), 409
        
        # Create new exchange request
        exchange_request = ExchangeRequest(
            requester_id=current_user_id,
            owner_id=book.user_id,
            book_id=book_id,
            message=message,
            status='pending'
        )
        
        db.session.add(exchange_request)
        db.session.commit()
        
        return jsonify({
            'message': 'Exchange request created successfully',
            'exchange': exchange_request.to_dict()
        }), 201
        
    except ValidationError as e:
        return jsonify({
            'error': 'Validation Error',
            'message': e.messages
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Failed to create exchange request'
        }), 500

@exchanges_bp.route('/<int:exchange_id>', methods=['PUT'])
@jwt_required()
def update_exchange(exchange_id):
    """Update exchange request status"""
    try:
        current_user_id = get_jwt_identity()
        
        # Validate input data
        data = exchange_update_schema.load(request.json)
        new_status = data['status']
        message = data.get('message')
        
        # Get the exchange request
        exchange = ExchangeRequest.query.get(exchange_id)
        if not exchange:
            return jsonify({
                'error': 'Not Found',
                'message': 'Exchange request not found'
            }), 404
        
        # Check authorization based on the action
        if new_status in ['approved', 'rejected']:
            # Only the book owner can approve/reject
            if exchange.owner_id != current_user_id:
                return jsonify({
                    'error': 'Forbidden',
                    'message': 'Only the book owner can approve or reject requests'
                }), 403
        elif new_status == 'completed':
            # Either party can mark as completed
            if exchange.requester_id != current_user_id and exchange.owner_id != current_user_id:
                return jsonify({
                    'error': 'Forbidden',
                    'message': 'Only parties involved in the exchange can mark it as completed'
                }), 403
        
        # Check if the current status allows the transition
        if exchange.status == 'rejected':
            return jsonify({
                'error': 'Bad Request',
                'message': 'Cannot update a rejected exchange request'
            }), 400
        
        if exchange.status == 'completed':
            return jsonify({
                'error': 'Bad Request',
                'message': 'Cannot update a completed exchange request'
            }), 400
        
        if new_status == 'completed' and exchange.status != 'approved':
            return jsonify({
                'error': 'Bad Request',
                'message': 'Exchange must be approved before it can be completed'
            }), 400
        
        # Update the exchange request
        old_status = exchange.status
        exchange.status = new_status
        if message:
            exchange.message = message
        
        # Update book availability when exchange is completed
        if new_status == 'completed':
            book = Book.query.get(exchange.book_id)
            if book:
                book.available = False  # Mark book as no longer available
        
        # If exchange is rejected, ensure book remains available
        elif new_status == 'rejected':
            book = Book.query.get(exchange.book_id)
            if book:
                # Check if there are other pending/approved requests for this book
                other_active_requests = ExchangeRequest.query.filter(
                    ExchangeRequest.book_id == exchange.book_id,
                    ExchangeRequest.id != exchange.id,
                    ExchangeRequest.status.in_(['pending', 'approved'])
                ).count()
                
                # If no other active requests, ensure book is available
                if other_active_requests == 0:
                    book.available = True
        
        db.session.commit()
        
        return jsonify({
            'message': f'Exchange request {new_status} successfully',
            'exchange': exchange.to_dict(),
            'status_changed': {
                'from': old_status,
                'to': new_status
            }
        }), 200
        
    except ValidationError as e:
        return jsonify({
            'error': 'Validation Error',
            'message': e.messages
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Failed to update exchange request'
        }), 500

@exchanges_bp.route('/<int:exchange_id>/history', methods=['GET'])
@jwt_required()
def get_exchange_history(exchange_id):
    """Get exchange history"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get the exchange request
        exchange = ExchangeRequest.query.get(exchange_id)
        if not exchange:
            return jsonify({
                'error': 'Not Found',
                'message': 'Exchange request not found'
            }), 404
        
        # Check if user is involved in this exchange
        if exchange.requester_id != current_user_id and exchange.owner_id != current_user_id:
            return jsonify({
                'error': 'Forbidden',
                'message': 'You can only view history of your own exchanges'
            }), 403
        
        # For now, return the exchange details with timestamps
        # In a more complex system, you might have a separate ExchangeHistory table
        history = {
            'exchange_id': exchange.id,
            'current_status': exchange.status,
            'created_at': exchange.created_at.isoformat(),
            'updated_at': exchange.updated_at.isoformat(),
            'timeline': [
                {
                    'status': 'pending',
                    'timestamp': exchange.created_at.isoformat(),
                    'description': 'Exchange request created'
                }
            ]
        }
        
        # Add status change events based on current status
        if exchange.status in ['approved', 'rejected', 'completed']:
            history['timeline'].append({
                'status': exchange.status,
                'timestamp': exchange.updated_at.isoformat(),
                'description': f'Exchange request {exchange.status}'
            })
        
        return jsonify({
            'history': history,
            'exchange': exchange.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Failed to retrieve exchange history'
        }), 500

@exchanges_bp.route('/<int:exchange_id>/cancel', methods=['DELETE'])
@jwt_required()
def cancel_exchange(exchange_id):
    """Cancel an exchange request"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get the exchange request
        exchange = ExchangeRequest.query.get(exchange_id)
        if not exchange:
            return jsonify({
                'error': 'Not Found',
                'message': 'Exchange request not found'
            }), 404
        
        # Only the requester can cancel their own request
        if exchange.requester_id != current_user_id:
            return jsonify({
                'error': 'Forbidden',
                'message': 'You can only cancel your own exchange requests'
            }), 403
        
        # Can only cancel pending requests
        if exchange.status != 'pending':
            return jsonify({
                'error': 'Bad Request',
                'message': f'Cannot cancel a {exchange.status} exchange request'
            }), 400
        
        # Delete the exchange request
        db.session.delete(exchange)
        
        # Ensure book availability is correct
        book = Book.query.get(exchange.book_id)
        if book:
            # Check if there are other pending/approved requests for this book
            other_active_requests = ExchangeRequest.query.filter(
                ExchangeRequest.book_id == exchange.book_id,
                ExchangeRequest.id != exchange.id,
                ExchangeRequest.status.in_(['pending', 'approved'])
            ).count()
            
            # If no other active requests, ensure book is available
            if other_active_requests == 0:
                book.available = True
        
        db.session.commit()
        
        return jsonify({
            'message': 'Exchange request cancelled successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Failed to cancel exchange request'
        }), 500


@exchanges_bp.route('/book/<int:book_id>/availability', methods=['PUT'])
@jwt_required()
def update_book_availability(book_id):
    """Update book availability status"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get the book
        book = Book.query.get(book_id)
        if not book:
            return jsonify({
                'error': 'Not Found',
                'message': 'Book not found'
            }), 404
        
        # Check ownership
        if book.user_id != current_user_id:
            return jsonify({
                'error': 'Forbidden',
                'message': 'You can only update availability of your own books'
            }), 403
        
        # Get the new availability status
        data = request.get_json()
        if not data or 'available' not in data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Available status is required'
            }), 400
        
        new_availability = data['available']
        if not isinstance(new_availability, bool):
            return jsonify({
                'error': 'Bad Request',
                'message': 'Available status must be true or false'
            }), 400
        
        # If setting to unavailable, reject all pending requests
        if not new_availability and book.available:
            pending_requests = ExchangeRequest.query.filter_by(
                book_id=book_id,
                status='pending'
            ).all()
            
            for request_obj in pending_requests:
                request_obj.status = 'rejected'
        
        # Update book availability
        book.available = new_availability
        db.session.commit()
        
        return jsonify({
            'message': 'Book availability updated successfully',
            'book': book.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Failed to update book availability'
        }), 500