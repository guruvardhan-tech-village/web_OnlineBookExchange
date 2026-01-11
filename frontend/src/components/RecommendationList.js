import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import recommendationService from '../services/recommendationService';
import BookCard from './BookCard';

const RecommendationList = ({ limit = 6, showTitle = true, className = '' }) => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchRecommendations();
    fetchStats();
  }, [limit]);

  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await recommendationService.getRecommendations(limit);
      setRecommendations(response.data.recommendations || []);
    } catch (err) {
      setError('Failed to load recommendations. Please try again later.');
      console.error('Error fetching recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await recommendationService.getRecommendationStats();
      setStats(response.data);
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  };

  const handleRefresh = async () => {
    try {
      setLoading(true);
      await recommendationService.refreshRecommendations();
      await fetchRecommendations();
    } catch (err) {
      setError('Failed to refresh recommendations.');
    }
  };

  const handleBookInteraction = async (bookId, interactionType) => {
    try {
      await recommendationService.recordInteraction(bookId, interactionType);
    } catch (err) {
      console.error('Failed to record interaction:', err);
    }
  };

  if (loading) {
    return (
      <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
        {showTitle && (
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-800">
              📚 Recommended for You
            </h2>
          </div>
        )}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(3)].map((_, index) => (
            <div key={index} className="animate-pulse">
              <div className="bg-gray-200 h-48 rounded-lg mb-4"></div>
              <div className="bg-gray-200 h-4 rounded mb-2"></div>
              <div className="bg-gray-200 h-4 rounded w-3/4"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
        {showTitle && (
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            📚 Recommended for You
          </h2>
        )}
        <div className="text-center py-8">
          <div className="text-red-500 mb-4">
            <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={fetchRecommendations}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (recommendations.length === 0) {
    return (
      <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
        {showTitle && (
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-800">
              📚 Recommended for You
            </h2>
            <button
              onClick={handleRefresh}
              className="text-blue-500 hover:text-blue-600 transition-colors"
              title="Refresh recommendations"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </button>
          </div>
        )}
        <div className="text-center py-8">
          <div className="text-gray-400 mb-4">
            <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-700 mb-2">No Recommendations Yet</h3>
          <p className="text-gray-600 mb-4">
            {stats && stats.total_interactions < 5 
              ? "Browse and interact with some books to get personalized recommendations!"
              : "We're working on finding books you'll love. Check back soon!"
            }
          </p>
          <Link
            to="/books"
            className="inline-block bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition-colors"
          >
            Browse Books
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
      {showTitle && (
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">
              📚 Recommended for You
            </h2>
            {stats && (
              <p className="text-sm text-gray-600 mt-1">
                Based on your {stats.total_interactions} interactions
                {stats.top_categories.length > 0 && (
                  <span> • Interested in {stats.top_categories[0].category}</span>
                )}
              </p>
            )}
          </div>
          <button
            onClick={handleRefresh}
            className="text-blue-500 hover:text-blue-600 transition-colors"
            title="Refresh recommendations"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {recommendations.map((recommendation, index) => (
          <div key={recommendation.book.id} className="relative">
            {/* Recommendation Badge */}
            <div className="absolute top-2 left-2 z-10 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-xs px-2 py-1 rounded-full shadow-lg">
              #{index + 1} • {Math.round(recommendation.relevance_score * 100)}% match
            </div>
            
            {/* Book Card */}
            <BookCard
              book={recommendation.book}
              onView={() => handleBookInteraction(recommendation.book.id, 'view')}
              onLike={() => handleBookInteraction(recommendation.book.id, 'like')}
              onRequest={() => handleBookInteraction(recommendation.book.id, 'request')}
              showActions={true}
            />
            
            {/* Recommendation Explanation */}
            <div className="mt-3 p-3 bg-gray-50 rounded-lg">
              <div className="flex items-start space-x-2">
                <div className="text-blue-500 mt-0.5">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <p className="text-sm text-gray-700">
                  {recommendation.recommendation_reason}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {recommendations.length >= limit && (
        <div className="text-center mt-6">
          <Link
            to="/recommendations"
            className="inline-block bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white px-6 py-2 rounded-lg transition-colors"
          >
            View All Recommendations
          </Link>
        </div>
      )}
    </div>
  );
};

export default RecommendationList;