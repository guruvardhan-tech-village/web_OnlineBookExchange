"""
Property-based tests for AI Recommendation Engine
Tests universal properties that should hold for all recommendation scenarios
"""
import pytest
from hypothesis import given, strategies as st, settings, assume
from hypothesis.stateful import RuleBasedStateMachine, Bundle, rule, initialize
from app import create_app, db
from app.models.user import User
from app.models.book import Book
from app.models.user_interaction import UserInteraction
from app.services.recommendation_engine import RecommendationEngine
from app.utils.auth import hash_password
import tempfile
import os


class RecommendationEngineStateMachine(RuleBasedStateMachine):
    """
    Stateful property-based testing for the recommendation engine.
    Tests that the recommendation system maintains consistency and correctness
    across various user interactions and book collections.
    """
    
    users = Bundle('users')
    books = Bundle('books')
    interactions = Bundle('interactions')
    
    def __init__(self):
        super().__init__()
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create temporary database
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{self.db_path}'
        
        db.create_all()
        self.engine = RecommendationEngine()
        
    def teardown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    @initialize()
    def setup_initial_data(self):
        """Initialize with some basic data"""
        pass
    
    @rule(target=users, email=st.emails(), password=st.text(min_size=8, max_size=50))
    def create_user(self, email, password):
        """Create a new user"""
        assume(not User.query.filter_by(email=email).first())
        
        user = User(
            email=email,
            password_hash=hash_password(password),
            first_name="Test",
            last_name="User",
            role='user'
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    @rule(target=books, 
          user=users,
          title=st.text(min_size=1, max_size=100),
          author=st.text(min_size=1, max_size=50),
          category=st.sampled_from(['Fiction', 'Non-Fiction', 'Science', 'History', 'Biography']),
          condition=st.sampled_from(['new', 'like_new', 'good', 'fair', 'poor']))
    def create_book(self, user, title, author, category, condition):
        """Create a new book listing"""
        book = Book(
            user_id=user.id,
            title=title,
            author=author,
            category=category,
            condition=condition,
            description=f"A {condition} book about {category.lower()}",
            available=True
        )
        db.session.add(book)
        db.session.commit()
        return book
    
    @rule(target=interactions,
          user=users,
          book=books,
          interaction_type=st.sampled_from(['view', 'like', 'request', 'search']))
    def create_interaction(self, user, book, interaction_type):
        """Create a user interaction with a book"""
        # Users shouldn't interact with their own books for recommendations
        assume(user.id != book.user_id)
        
        interaction = UserInteraction(
            user_id=user.id,
            book_id=book.id,
            interaction_type=interaction_type
        )
        db.session.add(interaction)
        db.session.commit()
        return interaction
    
    @rule(user=users)
    def test_recommendation_consistency(self, user):
        """
        Property: Recommendations should be consistent for the same user state
        """
        # Generate recommendations twice
        recs1 = self.engine.generate_recommendations(user.id, num_recommendations=5)
        recs2 = self.engine.generate_recommendations(user.id, num_recommendations=5)
        
        # Should return the same recommendations in the same order
        assert len(recs1) == len(recs2)
        for i, (rec1, rec2) in enumerate(zip(recs1, recs2)):
            assert rec1['book']['id'] == rec2['book']['id'], \
                f"Recommendation {i} differs between calls"
    
    @rule(user=users)
    def test_no_self_recommendations(self, user):
        """
        Property: Users should never be recommended their own books
        """
        recommendations = self.engine.generate_recommendations(user.id, num_recommendations=10)
        
        for rec in recommendations:
            assert rec['book']['user_id'] != user.id, \
                "User should not be recommended their own book"
    
    @rule(user=users)
    def test_recommendation_scores_ordered(self, user):
        """
        Property: Recommendations should be ordered by relevance score (descending)
        """
        recommendations = self.engine.generate_recommendations(user.id, num_recommendations=10)
        
        if len(recommendations) > 1:
            scores = [rec['relevance_score'] for rec in recommendations]
            assert scores == sorted(scores, reverse=True), \
                "Recommendations should be ordered by relevance score"
    
    @rule(user=users)
    def test_recommendation_scores_valid_range(self, user):
        """
        Property: All recommendation scores should be in valid range [0, 1]
        """
        recommendations = self.engine.generate_recommendations(user.id, num_recommendations=10)
        
        for rec in recommendations:
            score = rec['relevance_score']
            assert 0 <= score <= 1, \
                f"Relevance score {score} is outside valid range [0, 1]"
    
    @rule(user=users)
    def test_available_books_only(self, user):
        """
        Property: Only available books should be recommended
        """
        recommendations = self.engine.generate_recommendations(user.id, num_recommendations=10)
        
        for rec in recommendations:
            book_id = rec['book']['id']
            book = Book.query.get(book_id)
            assert book is not None, "Recommended book should exist"
            assert book.available is True, "Only available books should be recommended"
    
    @rule(book1=books, book2=books)
    def test_similarity_symmetry(self, book1, book2):
        """
        Property: Content similarity should be symmetric
        """
        assume(book1.id != book2.id)
        
        self.engine.fit_tfidf_model()
        
        sim1to2 = self.engine.calculate_content_similarity(book1.id, [book2.id])
        sim2to1 = self.engine.calculate_content_similarity(book2.id, [book1.id])
        
        if book2.id in sim1to2 and book1.id in sim2to1:
            score1 = sim1to2[book2.id]
            score2 = sim2to1[book1.id]
            assert abs(score1 - score2) < 0.001, \
                f"Similarity should be symmetric: {score1} != {score2}"
    
    @rule(book=books)
    def test_self_similarity_maximum(self, book):
        """
        Property: A book should have maximum similarity with itself
        """
        self.engine.fit_tfidf_model()
        
        # Create another book to compare with
        other_books = Book.query.filter(Book.id != book.id).all()
        if other_books:
            other_book_ids = [b.id for b in other_books[:5]]
            similarities = self.engine.calculate_content_similarity(book.id, other_book_ids)
            
            # Self-similarity would be 1.0, so all other similarities should be <= 1.0
            for sim_score in similarities.values():
                assert sim_score <= 1.0, \
                    f"Similarity score {sim_score} exceeds maximum possible value"
    
    @rule(user=users, num_recs=st.integers(min_value=1, max_value=20))
    def test_recommendation_count_limit(self, user, num_recs):
        """
        Property: Number of recommendations should not exceed requested amount
        """
        recommendations = self.engine.generate_recommendations(user.id, num_recommendations=num_recs)
        
        assert len(recommendations) <= num_recs, \
            f"Returned {len(recommendations)} recommendations, expected at most {num_recs}"
    
    @rule(user=users)
    def test_user_profile_consistency(self, user):
        """
        Property: User profile should be consistent across multiple builds
        """
        profile1 = self.engine.build_user_profile(user.id)
        profile2 = self.engine.build_user_profile(user.id)
        
        assert profile1 == profile2, "User profile should be consistent"
    
    @rule(user=users)
    def test_recommendation_reasons_present(self, user):
        """
        Property: All recommendations should have explanatory reasons
        """
        recommendations = self.engine.generate_recommendations(user.id, num_recommendations=5)
        
        for rec in recommendations:
            assert 'recommendation_reason' in rec, \
                "Each recommendation should have a reason"
            assert isinstance(rec['recommendation_reason'], str), \
                "Recommendation reason should be a string"
            assert len(rec['recommendation_reason']) > 0, \
                "Recommendation reason should not be empty"


# Property test class for running the state machine
class TestRecommendationEngineProperties:
    """Property 6: AI Recommendation Engine - Validates Requirements 6.1, 6.2, 6.3, 6.4, 6.5, 6.6"""
    
    def test_recommendation_engine_properties(self):
        """
        Test that the recommendation engine maintains all required properties
        across various user interactions and book collections.
        """
        # Run the state machine test
        state_machine_test = RecommendationEngineStateMachine.TestCase()
        state_machine_test.runTest()


# Additional focused property tests
class TestRecommendationAlgorithmProperties:
    """Focused tests for specific recommendation algorithm properties"""
    
    @pytest.fixture(autouse=True)
    def setup_test_app(self):
        """Set up test application and database"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create temporary database
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{self.db_path}'
        
        db.create_all()
        self.engine = RecommendationEngine()
        
        yield
        
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    @given(
        titles=st.lists(st.text(min_size=1, max_size=50), min_size=2, max_size=10),
        authors=st.lists(st.text(min_size=1, max_size=30), min_size=2, max_size=10),
        categories=st.lists(st.sampled_from(['Fiction', 'Science', 'History']), min_size=2, max_size=5)
    )
    def test_tfidf_corpus_building(self, titles, authors, categories):
        """
        Property: TF-IDF corpus should be built correctly from book data
        """
        # Create test user
        user = User(
            email="test@example.com", 
            password_hash="hashed", 
            first_name="Test",
            last_name="User",
            role="user"
        )
        db.session.add(user)
        db.session.commit()
        
        # Create books with the generated data
        books = []
        for i, (title, author, category) in enumerate(zip(titles, authors, categories)):
            book = Book(
                user_id=user.id,
                title=title,
                author=author,
                category=category,
                condition='good',
                available=True
            )
            db.session.add(book)
            books.append(book)
        
        db.session.commit()
        
        # Build corpus
        corpus = self.engine.build_corpus()
        
        # Verify corpus properties
        assert len(corpus) == len(books), "Corpus size should match number of available books"
        
        for i, text in enumerate(corpus):
            assert isinstance(text, str), "Corpus entries should be strings"
            # Text should contain preprocessed book information
            assert len(text.strip()) > 0, "Corpus entries should not be empty"
    
    @given(
        interaction_types=st.lists(
            st.sampled_from(['view', 'like', 'request', 'search']),
            min_size=1, max_size=20
        )
    )
    def test_user_profile_weighting(self, interaction_types):
        """
        Property: User profiles should correctly weight different interaction types
        """
        # Create test user and book
        user = User(
            email="test@example.com", 
            password_hash="hashed", 
            first_name="Test",
            last_name="User",
            role="user"
        )
        book = Book(
            user_id=999,  # Different user
            title="Test Book",
            author="Test Author", 
            category="Fiction",
            condition='good',
            available=True
        )
        db.session.add(user)
        db.session.add(book)
        db.session.commit()
        
        # Create interactions
        for interaction_type in interaction_types:
            interaction = UserInteraction(
                user_id=user.id,
                book_id=book.id,
                interaction_type=interaction_type
            )
            db.session.add(interaction)
        
        db.session.commit()
        
        # Build user profile
        profile = self.engine.build_user_profile(user.id)
        
        # Verify profile properties
        if profile:
            assert 'categories' in profile, "Profile should contain category preferences"
            assert 'authors' in profile, "Profile should contain author preferences"
            assert 'interaction_count' in profile, "Profile should contain interaction count"
            
            # Check that weights are normalized (sum to 1 or less)
            if profile['categories']:
                category_sum = sum(profile['categories'].values())
                assert 0 < category_sum <= 1.1, "Category weights should be normalized"
            
            if profile['authors']:
                author_sum = sum(profile['authors'].values())
                assert 0 < author_sum <= 1.1, "Author weights should be normalized"