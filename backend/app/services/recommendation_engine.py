"""
AI Recommendation Engine using TF-IDF and Cosine Similarity
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict, Counter
import re
from typing import List, Dict, Tuple, Optional
from ..models.book import Book
from ..models.user_interaction import UserInteraction
from .. import db


class RecommendationEngine:
    """
    AI-powered recommendation engine using TF-IDF vectorization and cosine similarity
    to provide personalized book recommendations based on user interaction history.
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=1.0  # Changed from 0.95 to handle small corpora
        )
        self.tfidf_matrix = None
        self.book_ids = []
        self.book_features = {}
        self.user_profiles = {}
        
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text for TF-IDF analysis by cleaning and normalizing.
        
        Args:
            text: Raw text to preprocess
            
        Returns:
            Cleaned and normalized text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits, keep only letters and spaces
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def build_corpus(self) -> List[str]:
        """
        Build text corpus from all available books for TF-IDF analysis.
        
        Returns:
            List of preprocessed text documents for each book
        """
        books = Book.query.filter_by(available=True).all()
        corpus = []
        self.book_ids = []
        self.book_features = {}
        
        for book in books:
            # Combine title, author, category, and description for rich content analysis
            text_content = f"{book.title} {book.author} {book.category}"
            if book.description:
                text_content += f" {book.description}"
            
            # Preprocess the combined text
            processed_text = self.preprocess_text(text_content)
            corpus.append(processed_text)
            
            # Store book metadata for later use
            self.book_ids.append(book.id)
            self.book_features[book.id] = {
                'title': book.title,
                'author': book.author,
                'category': book.category,
                'condition': book.condition,
                'description': book.description or '',
                'user_id': book.user_id
            }
        
        return corpus
    
    def fit_tfidf_model(self):
        """
        Fit the TF-IDF vectorizer on the book corpus and compute the TF-IDF matrix.
        """
        corpus = self.build_corpus()
        
        if not corpus:
            # Handle empty corpus case
            self.tfidf_matrix = np.array([]).reshape(0, 0)
            return
        
        # Adjust vectorizer parameters for small corpora
        if len(corpus) == 1:
            # For single document, use simpler parameters
            vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                min_df=1,
                max_df=1.0
            )
        else:
            # Use the configured vectorizer for larger corpora
            vectorizer = self.vectorizer
        
        # Fit and transform the corpus
        self.tfidf_matrix = vectorizer.fit_transform(corpus)
        
        # Update the vectorizer reference
        self.vectorizer = vectorizer
        
    def compute_similarity_matrix(self) -> np.ndarray:
        """
        Compute cosine similarity matrix between all books.
        
        Returns:
            Cosine similarity matrix where element (i,j) represents 
            similarity between book i and book j
        """
        if self.tfidf_matrix is None or self.tfidf_matrix.shape[0] == 0:
            return np.array([]).reshape(0, 0)
        
        # Compute cosine similarity matrix
        similarity_matrix = cosine_similarity(self.tfidf_matrix)
        return similarity_matrix
    
    def build_user_profile(self, user_id: int) -> Dict[str, float]:
        """
        Build user profile based on interaction history using weighted preferences.
        
        Args:
            user_id: ID of the user to build profile for
            
        Returns:
            Dictionary containing user preferences with weights
        """
        # Get user interactions from the last 90 days for relevancy
        interactions = UserInteraction.query.filter_by(user_id=user_id).all()
        
        if not interactions:
            return {}
        
        # Weight different interaction types
        interaction_weights = {
            'view': 1.0,
            'like': 2.0,
            'request': 3.0,
            'search': 0.5
        }
        
        # Aggregate preferences by category and author
        category_scores = defaultdict(float)
        author_scores = defaultdict(float)
        
        for interaction in interactions:
            book = Book.query.get(interaction.book_id)
            if not book:
                continue
                
            weight = interaction_weights.get(interaction.interaction_type, 1.0)
            
            # Accumulate category preferences
            category_scores[book.category] += weight
            
            # Accumulate author preferences
            author_scores[book.author] += weight
        
        # Normalize scores
        total_category_score = sum(category_scores.values()) or 1
        total_author_score = sum(author_scores.values()) or 1
        
        normalized_categories = {
            cat: score / total_category_score 
            for cat, score in category_scores.items()
        }
        normalized_authors = {
            author: score / total_author_score 
            for author, score in author_scores.items()
        }
        
        return {
            'categories': normalized_categories,
            'authors': normalized_authors,
            'interaction_count': len(interactions)
        }
    
    def calculate_content_similarity(self, book_id: int, target_books: List[int]) -> Dict[int, float]:
        """
        Calculate content-based similarity scores between a book and target books.
        
        Args:
            book_id: ID of the reference book
            target_books: List of book IDs to compare against
            
        Returns:
            Dictionary mapping book IDs to similarity scores
        """
        if book_id not in self.book_ids:
            return {}
        
        book_index = self.book_ids.index(book_id)
        similarity_matrix = self.compute_similarity_matrix()
        
        if similarity_matrix.shape[0] == 0:
            return {}
        
        similarities = {}
        for target_id in target_books:
            if target_id in self.book_ids and target_id != book_id:
                target_index = self.book_ids.index(target_id)
                similarities[target_id] = float(similarity_matrix[book_index][target_index])
        
        return similarities
    
    def generate_recommendations(self, user_id: int, num_recommendations: int = 10) -> List[Dict]:
        """
        Generate personalized book recommendations for a user.
        
        Args:
            user_id: ID of the user to generate recommendations for
            num_recommendations: Number of recommendations to return
            
        Returns:
            List of recommended books with relevance scores
        """
        # Ensure TF-IDF model is fitted
        self.fit_tfidf_model()
        
        # Build user profile
        user_profile = self.build_user_profile(user_id)
        
        if not user_profile or not self.book_ids:
            # Return popular books if no user history
            return self._get_popular_books(num_recommendations)
        
        # Get books user has already interacted with
        user_interactions = UserInteraction.query.filter_by(user_id=user_id).all()
        interacted_book_ids = {interaction.book_id for interaction in user_interactions}
        
        # Get available books excluding user's own books and already interacted books
        available_books = Book.query.filter(
            Book.available == True,
            Book.user_id != user_id,
            ~Book.id.in_(interacted_book_ids)
        ).all()
        
        if not available_books:
            return []
        
        # Calculate recommendation scores
        book_scores = {}
        
        for book in available_books:
            score = 0.0
            
            # Category preference score
            category_pref = user_profile.get('categories', {}).get(book.category, 0)
            score += category_pref * 0.4
            
            # Author preference score
            author_pref = user_profile.get('authors', {}).get(book.author, 0)
            score += author_pref * 0.3
            
            # Content similarity score (based on books user liked)
            content_score = self._calculate_user_content_similarity(user_id, book.id)
            score += content_score * 0.3
            
            book_scores[book.id] = score
        
        # Sort by score and return top recommendations
        sorted_books = sorted(book_scores.items(), key=lambda x: x[1], reverse=True)
        top_book_ids = [book_id for book_id, _ in sorted_books[:num_recommendations]]
        
        # Fetch book details and format response
        recommendations = []
        for book_id in top_book_ids:
            book = Book.query.get(book_id)
            if book:
                recommendations.append({
                    'book': book.to_dict(),
                    'relevance_score': round(book_scores[book_id], 3),
                    'recommendation_reason': self._generate_reason(user_profile, book)
                })
        
        return recommendations
    
    def _calculate_user_content_similarity(self, user_id: int, book_id: int) -> float:
        """
        Calculate content similarity between a book and books the user has liked.
        
        Args:
            user_id: ID of the user
            book_id: ID of the book to score
            
        Returns:
            Average similarity score
        """
        # Get books user has liked or requested
        liked_interactions = UserInteraction.query.filter(
            UserInteraction.user_id == user_id,
            UserInteraction.interaction_type.in_(['like', 'request'])
        ).all()
        
        if not liked_interactions:
            return 0.0
        
        liked_book_ids = [interaction.book_id for interaction in liked_interactions]
        similarities = self.calculate_content_similarity(book_id, liked_book_ids)
        
        if not similarities:
            return 0.0
        
        # Return average similarity to liked books
        return sum(similarities.values()) / len(similarities)
    
    def _generate_reason(self, user_profile: Dict, book: Book) -> str:
        """
        Generate explanation for why a book was recommended.
        
        Args:
            user_profile: User's preference profile
            book: Book being recommended
            
        Returns:
            Human-readable recommendation reason
        """
        reasons = []
        
        # Check category preference
        category_pref = user_profile.get('categories', {}).get(book.category, 0)
        if category_pref > 0.1:
            reasons.append(f"you've shown interest in {book.category} books")
        
        # Check author preference
        author_pref = user_profile.get('authors', {}).get(book.author, 0)
        if author_pref > 0.1:
            reasons.append(f"you've liked books by {book.author}")
        
        if not reasons:
            reasons.append("based on your reading preferences")
        
        return "Recommended because " + " and ".join(reasons)
    
    def _get_popular_books(self, num_books: int) -> List[Dict]:
        """
        Get popular books based on interaction count for new users.
        
        Args:
            num_books: Number of books to return
            
        Returns:
            List of popular books
        """
        # Get books with most interactions
        popular_books = db.session.query(Book, db.func.count(UserInteraction.id).label('interaction_count'))\
            .outerjoin(UserInteraction)\
            .filter(Book.available == True)\
            .group_by(Book.id)\
            .order_by(db.desc('interaction_count'))\
            .limit(num_books)\
            .all()
        
        recommendations = []
        for book, count in popular_books:
            recommendations.append({
                'book': book.to_dict(),
                'relevance_score': 0.5,  # Default score for popular books
                'recommendation_reason': f"Popular book with {count} interactions"
            })
        
        return recommendations
    
    def update_model(self):
        """
        Update the recommendation model with latest data.
        Should be called periodically or when significant data changes occur.
        """
        self.fit_tfidf_model()
        # Clear cached user profiles to force rebuild
        self.user_profiles.clear()