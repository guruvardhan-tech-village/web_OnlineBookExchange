from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app import db
from app.models.book import Book
from app.models.exchange_request import ExchangeRequest
from app.schemas.book import book_create_schema, book_update_schema

books_bp = Blueprint('books', __name__)

@books_bp.route('/search', methods=['GET'])
def search_books():
    """Advanced search endpoint with enhanced filtering"""
    try:
        # Get search parameters
        query_text = request.args.get('q', '').strip()
        category = request.args.get('category')
        condition = request.args.get('condition')
        author = request.args.get('author')
        title = request.args.get('title')
        min_year = request.args.get('min_year', type=int)
        max_year = request.args.get('max_year', type=int)
        available_only = request.args.get('available', 'true').lower() == 'true'
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        # Build query
        query = Book.query
        
        # Apply availability filter
        if available_only:
            query = query.filter(Book.available == True)
        
        # Apply specific field filters
        if category:
            query = query.filter(Book.category.ilike(f'%{category}%'))
        
        if condition:
            query = query.filter(Book.condition == condition)
        
        if author:
            query = query.filter(Book.author.ilike(f'%{author}%'))
        
        if title:
            query = query.filter(Book.title.ilike(f'%{title}%'))
        
        # Apply date range filters if provided
        if min_year:
            from datetime import datetime
            start_date = datetime(min_year, 1, 1)
            query = query.filter(Book.created_at >= start_date)
        
        if max_year:
            from datetime import datetime
            end_date = datetime(max_year, 12, 31, 23, 59, 59)
            query = query.filter(Book.created_at <= end_date)
        
        # Apply general text search if provided
        if query_text:
            search_term = f'%{query_text}%'
            query = query.filter(
                db.or_(
                    Book.title.ilike(search_term),
                    Book.author.ilike(search_term),
                    Book.category.ilike(search_term),
                    Book.description.ilike(search_term)
                )
            )
        
        # Order by relevance (books with search term in title first, then by date)
        if query_text:
            query = query.order_by(
                Book.title.ilike(f'%{query_text}%').desc(),
                Book.created_at.desc()
            )
        else:
            query = query.order_by(Book.created_at.desc())
        
        # Execute query with pagination
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        books = [book.to_dict() for book in pagination.items]
        
        return jsonify({
            'books': books,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            },
            'search_params': {
                'query': query_text,
                'category': category,
                'condition': condition,
                'author': author,
                'title': title,
                'available_only': available_only
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Failed to search books'
        }), 500


@books_bp.route('', methods=['GET'])
def get_books():
    """Get all books with pagination and filtering"""
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)  # Max 100 per page
        
        # Get filter parameters
        category = request.args.get('category')
        condition = request.args.get('condition')
        author = request.args.get('author')
        title = request.args.get('title')
        search = request.args.get('search')  # General search across multiple fields
        available_only = request.args.get('available', 'true').lower() == 'true'
        
        # Build query
        query = Book.query
        
        # Apply filters
        if available_only:
            query = query.filter(Book.available == True)
        
        if category:
            query = query.filter(Book.category.ilike(f'%{category}%'))
        
        if condition:
            query = query.filter(Book.condition == condition)
        
        if author:
            query = query.filter(Book.author.ilike(f'%{author}%'))
        
        if title:
            query = query.filter(Book.title.ilike(f'%{title}%'))
        
        if search:
            # General search across title, author, category, and description
            search_term = f'%{search}%'
            query = query.filter(
                db.or_(
                    Book.title.ilike(search_term),
                    Book.author.ilike(search_term),
                    Book.category.ilike(search_term),
                    Book.description.ilike(search_term)
                )
            )
        
        # Order by creation date (newest first)
        query = query.order_by(Book.created_at.desc())
        
        # Paginate results
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        books = [book.to_dict() for book in pagination.items]
        
        return jsonify({
            'books': books,
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
            'message': 'Failed to retrieve books'
        }), 500

@books_bp.route('', methods=['POST'])
@jwt_required()
def create_book():
    """Create a new book listing"""
    try:
        # Get current user ID from JWT token
        current_user_id = get_jwt_identity()
        
        # Validate input data
        data = book_create_schema.load(request.json)
        
        # Create new book instance
        book = Book(
            user_id=current_user_id,
            title=data['title'],
            author=data['author'],
            isbn=data.get('isbn'),
            category=data['category'],
            condition=data['condition'],
            description=data.get('description'),
            image_url=data.get('image_url')
        )
        
        # Save to database
        db.session.add(book)
        db.session.commit()
        
        return jsonify({
            'message': 'Book listing created successfully',
            'book': book.to_dict()
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
            'message': 'Failed to create book listing'
        }), 500

@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get specific book details"""
    try:
        book = Book.query.get(book_id)
        
        if not book:
            return jsonify({
                'error': 'Not Found',
                'message': 'Book not found'
            }), 404
        
        return jsonify({
            'book': book.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Failed to retrieve book'
        }), 500

@books_bp.route('/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    """Update book listing"""
    try:
        # Get current user ID from JWT token
        current_user_id = get_jwt_identity()
        
        # Find the book
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
                'message': 'You can only update your own book listings'
            }), 403
        
        # Validate input data
        data = book_update_schema.load(request.json)
        
        # Update book fields
        for field, value in data.items():
            if hasattr(book, field):
                setattr(book, field, value)
        
        # Save changes
        db.session.commit()
        
        return jsonify({
            'message': 'Book listing updated successfully',
            'book': book.to_dict()
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
            'message': 'Failed to update book listing'
        }), 500

@books_bp.route('/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    """Delete book listing"""
    try:
        # Get current user ID from JWT token
        current_user_id = get_jwt_identity()
        
        # Find the book
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
                'message': 'You can only delete your own book listings'
            }), 403
        
        # Handle cascade deletion of related exchange requests
        # Update status of pending exchange requests to 'rejected' before deletion
        pending_requests = ExchangeRequest.query.filter_by(
            book_id=book_id, 
            status='pending'
        ).all()
        
        for request_obj in pending_requests:
            request_obj.status = 'rejected'
        
        # Delete all exchange requests for this book
        ExchangeRequest.query.filter_by(book_id=book_id).delete()
        
        # Delete the book
        db.session.delete(book)
        db.session.commit()
        
        return jsonify({
            'message': 'Book listing deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Failed to delete book listing'
        }), 500

@books_bp.route('/upload-image', methods=['POST'])
@jwt_required()
def upload_image():
    """Upload book image"""
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({
                'error': 'Bad Request',
                'message': 'No image file provided'
            }), 400
        
        file = request.files['image']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({
                'error': 'Bad Request',
                'message': 'No file selected'
            }), 400
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if not file.filename or '.' not in file.filename:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Invalid file format'
            }), 400
        
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        if file_extension not in allowed_extensions:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Invalid file type. Allowed types: png, jpg, jpeg, gif'
            }), 400
        
        # Check file size (5MB limit)
        file.seek(0, 2)  # Seek to end of file
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        max_size = 5 * 1024 * 1024  # 5MB
        if file_size > max_size:
            return jsonify({
                'error': 'Bad Request',
                'message': 'File size exceeds 5MB limit'
            }), 400
        
        # Generate unique filename
        import uuid
        import os
        from werkzeug.utils import secure_filename
        
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        # Create uploads directory if it doesn't exist
        upload_dir = 'uploads'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # Save file
        file_path = os.path.join(upload_dir, unique_filename)
        file.save(file_path)
        
        # Return the image URL
        image_url = f"/uploads/{unique_filename}"
        
        return jsonify({
            'message': 'Image uploaded successfully',
            'image_url': image_url
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Failed to upload image'
        }), 500