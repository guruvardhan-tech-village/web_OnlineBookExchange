import React, { useState, useEffect } from 'react';
import BookCard from './BookCard';
import bookService from '../services/bookService';

const BookList = ({ 
  searchQuery = '', 
  filters = {}, 
  onBookSelect,
  onRequestExchange,
  showOwnerActions = false,
  onEdit,
  onDelete
}) => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 12,
    total: 0,
    pages: 0
  });

  const fetchBooks = async (page = 1) => {
    setLoading(true);
    setError(null);
    
    try {
      const params = {
        page,
        per_page: pagination.per_page,
        ...filters
      };

      let response;
      if (searchQuery && searchQuery.trim()) {
        // Use search endpoint when there's a search query
        response = await bookService.searchBooks(searchQuery.trim(), params);
      } else {
        // Use regular listing endpoint when no search query
        response = await bookService.getBooks(params);
      }

      setBooks(response.books || []);
      setPagination({
        page: response.page || 1,
        per_page: response.per_page || 12,
        total: response.total || 0,
        pages: response.pages || 0
      });
    } catch (err) {
      setError(err.message);
      setBooks([]);
    } finally {
      setLoading(false);
    }
  };

  // Fetch books when component mounts or dependencies change
  useEffect(() => {
    fetchBooks(1);
  }, [searchQuery, filters]); // eslint-disable-line react-hooks/exhaustive-deps

  const handlePageChange = (newPage) => {
    if (newPage >= 1 && newPage <= pagination.pages) {
      fetchBooks(newPage);
    }
  };

  const handleRefresh = () => {
    fetchBooks(pagination.page);
  };

  const handleBookAction = async (action, book) => {
    try {
      switch (action) {
        case 'edit':
          if (onEdit) onEdit(book);
          break;
        case 'delete':
          if (onDelete) {
            await onDelete(book);
            // Refresh the list after deletion
            handleRefresh();
          }
          break;
        case 'request':
          if (onRequestExchange) onRequestExchange(book);
          break;
        case 'select':
          if (onBookSelect) onBookSelect(book);
          break;
        default:
          break;
      }
    } catch (err) {
      setError(err.message);
    }
  };

  // Loading state
  if (loading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {[...Array(8)].map((_, index) => (
            <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden animate-pulse">
              <div className="w-full h-48 bg-gray-200"></div>
              <div className="p-4 space-y-3">
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                <div className="flex gap-2">
                  <div className="h-6 bg-gray-200 rounded w-16"></div>
                  <div className="h-6 bg-gray-200 rounded w-16"></div>
                </div>
                <div className="h-3 bg-gray-200 rounded w-full"></div>
                <div className="h-8 bg-gray-200 rounded w-full"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="text-center py-12">
        <div className="bg-red-50 border border-red-200 rounded-md p-6 max-w-md mx-auto">
          <div className="flex items-center justify-center w-12 h-12 mx-auto mb-4 bg-red-100 rounded-full">
            <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-red-800 mb-2">Error Loading Books</h3>
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={handleRefresh}
            className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  // Empty state
  if (books.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="max-w-md mx-auto">
          <div className="flex items-center justify-center w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full">
            <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Books Found</h3>
          <p className="text-gray-600 mb-4">
            {searchQuery && searchQuery.trim() !== '' 
              ? `No books found for "${searchQuery}". Try different keywords or adjust your filters.`
              : Object.keys(filters).length > 0
              ? 'No books match your current filters. Try adjusting your filter criteria.'
              : 'No books are currently available. Be the first to add a book!'}
          </p>
          {searchQuery || Object.keys(filters).length > 0 ? (
            <button
              onClick={() => window.location.reload()}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Clear Filters
            </button>
          ) : null}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Results Summary */}
      <div className="flex items-center justify-between">
        <div className="text-sm text-gray-600">
          Showing {((pagination.page - 1) * pagination.per_page) + 1} to{' '}
          {Math.min(pagination.page * pagination.per_page, pagination.total)} of{' '}
          {pagination.total} books
        </div>
        <button
          onClick={handleRefresh}
          className="text-sm text-blue-600 hover:text-blue-700 font-medium"
        >
          Refresh
        </button>
      </div>

      {/* Books Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {books.map((book) => (
          <BookCard
            key={book.id}
            book={book}
            onRequestExchange={() => handleBookAction('request', book)}
            onEdit={() => handleBookAction('edit', book)}
            onDelete={() => handleBookAction('delete', book)}
            showOwnerActions={showOwnerActions}
            onClick={() => handleBookAction('select', book)}
          />
        ))}
      </div>

      {/* Pagination */}
      {pagination.pages > 1 && (
        <div className="flex items-center justify-center space-x-2 pt-6">
          <button
            onClick={() => handlePageChange(pagination.page - 1)}
            disabled={pagination.page <= 1}
            className={`px-3 py-2 text-sm font-medium rounded-md ${
              pagination.page <= 1
                ? 'text-gray-400 cursor-not-allowed'
                : 'text-gray-700 hover:text-blue-600'
            }`}
          >
            Previous
          </button>

          {/* Page Numbers */}
          <div className="flex space-x-1">
            {[...Array(pagination.pages)].map((_, index) => {
              const pageNum = index + 1;
              const isCurrentPage = pageNum === pagination.page;
              
              // Show first page, last page, current page, and pages around current
              const showPage = 
                pageNum === 1 ||
                pageNum === pagination.pages ||
                (pageNum >= pagination.page - 1 && pageNum <= pagination.page + 1);

              if (!showPage) {
                // Show ellipsis for gaps
                if (pageNum === pagination.page - 2 || pageNum === pagination.page + 2) {
                  return (
                    <span key={pageNum} className="px-3 py-2 text-sm text-gray-400">
                      ...
                    </span>
                  );
                }
                return null;
              }

              return (
                <button
                  key={pageNum}
                  onClick={() => handlePageChange(pageNum)}
                  className={`px-3 py-2 text-sm font-medium rounded-md ${
                    isCurrentPage
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-700 hover:text-blue-600 hover:bg-blue-50'
                  }`}
                >
                  {pageNum}
                </button>
              );
            })}
          </div>

          <button
            onClick={() => handlePageChange(pagination.page + 1)}
            disabled={pagination.page >= pagination.pages}
            className={`px-3 py-2 text-sm font-medium rounded-md ${
              pagination.page >= pagination.pages
                ? 'text-gray-400 cursor-not-allowed'
                : 'text-gray-700 hover:text-blue-600'
            }`}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default BookList;