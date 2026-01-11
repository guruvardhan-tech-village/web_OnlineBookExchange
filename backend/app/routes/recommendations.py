"""
Recommendation API routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError
from ..services.recommendation_engine import RecommendationEngine
from ..models.user_interaction import UserInteraction
from ..models.book import Book
from .. import db

recommendations_bp = Blueprint('recommendations', __name__)

# Initialize recommendation engine
recommendation_engine = RecommendationEngine()


class RecommendationQuerySchema(Schema):
    """Schema for recommendation query parameters"""
    limit = fields.Integer(load_default=10, validate=lambda x: 1 <= x <= 50)


class InteractionSchema(Schema):
    """Schema for user interaction tracking"""
    book_id = fields.Integer(required=True)
    interaction_type = fields.String(
        required=True,
        validate=lambda x: x in ['view', 'like', 'request', 'search']
    )


@recommendations_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    """
    Get personalized book recommendations for the authenticated user.
    
    Query Parameters:
        limit (int): Number of recommendations to return (1-50, default: 10)
    
    Returns:
        JSON response with personalized book recommendations
    """
    try:
        # Validate query parameters
        schema = RecommendationQuerySchema()
        args = schema.load(request.args)
        
        user_id = get_jwt_identity()
        limit = args['limit']
        
        # Generate recommendations
        recommendations = recommendation_engine.generate_recommendations(
            user_id=user_id,
            num_recommendations=limit
        )
        
        return jsonify({
            'success': True,
            'data': {
                'recommendations': recommendations,
                'count': len(recommendations),
                'user_id': user_id
            }
        }), 200
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'Invalid query parameters',
            'details': e.messages
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to generate recommendations',
            'details': str(e)
        }), 500


@recommendations_bp.route('/recommendations/similar/<int:book_id>', methods=['GET'])
@jwt_required()
def get_similar_books(book_id):
    """
    Get books similar to a specific book based on content similarity.
    
    Args:
        book_id (int): ID of the book to find similar books for
    
    Query Parameters:
        limit (int): Number of similar books to return (1-50, default: 10)
    
    Returns:
        JSON response with similar books
    """
    try:
        # Validate query parameters
        schema = RecommendationQuerySchema()
        args = schema.load(request.args)
        
        user_id = get_jwt_identity()
        limit = args['limit']
        
        # Check if book exists
        book = Book.query.get(book_id)
        if not book:
            return jsonify({
                'success': False,
                'error': 'Book not found'
            }), 404
        
        # Ensure recommendation engine is fitted
        recommendation_engine.fit_tfidf_model()
        
        # Get all available books except the reference book and user's own books
        available_books = Book.query.filter(
            Book.available == True,
            Book.id != book_id,
            Book.user_id != user_id
        ).all()
        
        if not available_books:
            return jsonify({
                'success': True,
                'data': {
                    'similar_books': [],
                    'count': 0,
                    'reference_book': book.to_dict()
                }
            }), 200
        
        # Calculate similarities
        target_book_ids = [b.id for b in available_books]
        similarities = recommendation_engine.calculate_content_similarity(
            book_id, target_book_ids
        )
        
        # Sort by similarity and get top results
        sorted_similarities = sorted(
            similarities.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:limit]
        
        # Format response
        similar_books = []
        for similar_book_id, similarity_score in sorted_similarities:
            similar_book = Book.query.get(similar_book_id)
            if similar_book:
                similar_books.append({
                    'book': similar_book.to_dict(),
                    'similarity_score': round(similarity_score, 3)
                })
        
        return jsonify({
            'success': True,
            'data': {
                'similar_books': similar_books,
                'count': len(similar_books),
                'reference_book': book.to_dict()
            }
        }), 200
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'Invalid query parameters',
            'details': e.messages
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to find similar books',
            'details': str(e)
        }), 500


@recommendations_bp.route('/interactions', methods=['POST'])
@jwt_required()
def record_interaction():
    """
    Record user interaction with a book for recommendation tracking.
    
    Request Body:
        book_id (int): ID of the book interacted with
        interaction_type (str): Type of interaction ('view', 'like', 'request', 'search')
    
    Returns:
        JSON response confirming interaction recording
    """
    try:
        # Validate request data
        schema = InteractionSchema()
        data = schema.load(request.get_json())
        
        user_id = get_jwt_identity()
        book_id = data['book_id']
        interaction_type = data['interaction_type']
        
        # Check if book exists
        book = Book.query.get(book_id)
        if not book:
            return jsonify({
                'success': False,
                'error': 'Book not found'
            }), 404
        
        # Prevent duplicate interactions within a short time frame
        # (e.g., multiple views of the same book within 5 minutes)
        if interaction_type == 'view':
            from datetime import datetime, timedelta
            recent_cutoff = datetime.utcnow() - timedelta(minutes=5)
            
            existing_interaction = UserInteraction.query.filter(
                UserInteraction.user_id == user_id,
                UserInteraction.book_id == book_id,
                UserInteraction.interaction_type == 'view',
                UserInteraction.created_at > recent_cutoff
            ).first()
            
            if existing_interaction:
                return jsonify({
                    'success': True,
                    'message': 'Interaction already recorded recently'
                }), 200
        
        # Create new interaction record
        interaction = UserInteraction(
            user_id=user_id,
            book_id=book_id,
            interaction_type=interaction_type
        )
        
        db.session.add(interaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'interaction': interaction.to_dict(),
                'message': 'Interaction recorded successfully'
            }
        }), 201
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'Invalid request data',
            'details': e.messages
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to record interaction',
            'details': str(e)
        }), 500


@recommendations_bp.route('/recommendations/refresh', methods=['POST'])
@jwt_required()
def refresh_recommendations():
    """
    Refresh the recommendation model with latest data.
    This endpoint can be called to update the model when significant data changes occur.
    
    Returns:
        JSON response confirming model refresh
    """
    try:
        user_id = get_jwt_identity()
        
        # Update the recommendation model
        recommendation_engine.update_model()
        
        return jsonify({
            'success': True,
            'message': 'Recommendation model refreshed successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to refresh recommendation model',
            'details': str(e)
        }), 500


@recommendations_bp.route('/recommendations/stats', methods=['GET'])
@jwt_required()
def get_recommendation_stats():
    """
    Get recommendation statistics for the authenticated user.
    
    Returns:
        JSON response with user's interaction statistics
    """
    try:
        user_id = get_jwt_identity()
        
        # Get user interaction statistics
        total_interactions = UserInteraction.query.filter_by(user_id=user_id).count()
        
        interaction_counts = db.session.query(
            UserInteraction.interaction_type,
            db.func.count(UserInteraction.id).label('count')
        ).filter_by(user_id=user_id).group_by(UserInteraction.interaction_type).all()
        
        interaction_breakdown = {
            interaction_type: count 
            for interaction_type, count in interaction_counts
        }
        
        # Get user's preferred categories based on interactions
        category_preferences = db.session.query(
            Book.category,
            db.func.count(UserInteraction.id).label('count')
        ).join(UserInteraction, Book.id == UserInteraction.book_id)\
         .filter(UserInteraction.user_id == user_id)\
         .group_by(Book.category)\
         .order_by(db.desc('count'))\
         .limit(5).all()
        
        top_categories = [
            {'category': category, 'interaction_count': count}
            for category, count in category_preferences
        ]
        
        return jsonify({
            'success': True,
            'data': {
                'total_interactions': total_interactions,
                'interaction_breakdown': interaction_breakdown,
                'top_categories': top_categories,
                'has_sufficient_data': total_interactions >= 5
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get recommendation statistics',
            'details': str(e)
        }), 500