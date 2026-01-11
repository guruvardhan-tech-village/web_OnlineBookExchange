import React, { useState, useEffect } from 'react';
import recommendationService from '../services/recommendationService';
import BookCard from './BookCard';

const SimilarBooks = ({ bookId, limit = 4, className = '' }) => {
  const [similarBooks, setSimilarBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (bookId) {
      fetchSimilarBooks();
    }
  }, [bookId, limit]);

  const fetchSimilarBooks = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await recommendationService.getSimilarBooks(bookId, limit);
      setSimilarBooks(response.data.similar_books || []);
    } catch (err) {
      setError('Failed to load similar books.');
      console.error('Error fetching similar books:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Similar Books</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[...Array(limit)].map((_, index) => (
            <div key={index} className="animate-pulse">
              <div className="bg-gray-200 h-32 rounded-lg mb-2"></div>
              <div className="bg-gray-200 h-4 rounded mb-1"></div>
              <div className="bg-gray-200 h-3 rounded w-3/4"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Similar Books</h3>
        <div className="text-center py-4">
          <p className="text-gray-600">{error}</p>
          <button
            onClick={fetchSimilarBooks}
            className="mt-2 text-blue-500 hover:text-blue-600 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (similarBooks.length === 0) {
    return (
      <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Similar Books</h3>
        <div className="text-center py-4">
          <p className="text-gray-600">No similar books found.</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Similar Books
        <span className="text-sm font-normal text-gray-600 ml-2">
          Based on content similarity
        </span>
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {similarBooks.map((similarBook, index) => (
          <div key={similarBook.book.id} className="relative">
            {/* Similarity Badge */}
            <div className="absolute top-2 left-2 z-10 bg-blue-500 text-white text-xs px-2 py-1 rounded-full">
              {Math.round(similarBook.similarity_score * 100)}% match
            </div>
            
            {/* Book Card */}
            <BookCard
              book={similarBook.book}
              showActions={true}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default SimilarBooks;