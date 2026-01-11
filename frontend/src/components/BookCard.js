import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import useInteractionTracking from '../hooks/useInteractionTracking';
import ExchangeRequestForm from './ExchangeRequestForm';

const BookCard = ({ 
  book, 
  onRequestExchange, 
  onEdit, 
  onDelete, 
  onView,
  onLike,
  onRequest,
  showActions = true,
  showOwnerActions = false 
}) => {
  const { user } = useAuth();
  const { trackView, trackLike, trackRequest } = useInteractionTracking();
  const [showExchangeForm, setShowExchangeForm] = useState(false);
  const [isLiked, setIsLiked] = useState(false);
  const isOwner = user && book.user_id === user.id;

  // Track view when component mounts
  useEffect(() => {
    if (book.id && !isOwner) {
      trackView(book.id);
      if (onView) {
        onView(book.id);
      }
    }
  }, [book.id, isOwner, trackView, onView]);

  const getConditionColor = (condition) => {
    switch (condition?.toLowerCase()) {
      case 'new':
        return 'bg-green-100 text-green-800';
      case 'like_new':
        return 'bg-blue-100 text-blue-800';
      case 'good':
        return 'bg-yellow-100 text-yellow-800';
      case 'fair':
        return 'bg-orange-100 text-orange-800';
      case 'poor':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const handleLike = async () => {
    if (!isOwner && book.id) {
      setIsLiked(!isLiked);
      await trackLike(book.id);
      if (onLike) {
        onLike(book.id);
      }
    }
  };

  const handleRequestExchange = async () => {
    if (!isOwner && book.id) {
      await trackRequest(book.id);
      if (onRequest) {
        onRequest(book.id);
      }
    }

    if (onRequestExchange) {
      onRequestExchange(book);
    } else {
      setShowExchangeForm(true);
    }
  };

  const handleExchangeSuccess = (exchange) => {
    setShowExchangeForm(false);
    if (onRequestExchange) {
      onRequestExchange(book, exchange);
    }
  };

  const handleExchangeCancel = () => {
    setShowExchangeForm(false);
  };

  const handleEdit = () => {
    if (onEdit) {
      onEdit(book);
    }
  };

  const handleDelete = () => {
    if (onDelete) {
      onDelete(book);
    }
  };

  const formatCondition = (condition) => {
    return condition?.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()) || 'Unknown';
  };

  return (
    <>
      <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
        {/* Book Image */}
        <div className="aspect-w-3 aspect-h-4 bg-gray-200 relative">
          {book.image_url ? (
            <img
              src={book.image_url}
              alt={`Cover of ${book.title}`}
              className="w-full h-48 object-cover"
              onError={(e) => {
                e.target.src = '/placeholder-book.png';
              }}
            />
          ) : (
            <div className="w-full h-48 bg-gray-200 flex items-center justify-center">
              <svg
                className="w-12 h-12 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                />
              </svg>
            </div>
          )}
          
          {/* Like Button */}
          {!isOwner && showActions && (
            <button
              onClick={handleLike}
              className={`absolute top-2 right-2 p-2 rounded-full transition-colors ${
                isLiked 
                  ? 'bg-red-500 text-white' 
                  : 'bg-white bg-opacity-80 text-gray-600 hover:bg-red-500 hover:text-white'
              }`}
            >
              <svg className="w-4 h-4" fill={isLiked ? 'currentColor' : 'none'} stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </button>
          )}
        </div>

        {/* Book Details */}
        <div className="p-4">
          {/* Title and Author */}
          <div className="mb-2">
            <h3 className="text-lg font-semibold text-gray-900 line-clamp-2">
              {book.title}
            </h3>
            <p className="text-sm text-gray-600 mt-1">
              by {book.author}
            </p>
          </div>

          {/* Category and Condition */}
          <div className="flex items-center gap-2 mb-3">
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              {book.category}
            </span>
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getConditionColor(book.condition)}`}>
              {formatCondition(book.condition)}
            </span>
          </div>

          {/* Description */}
          {book.description && (
            <p className="text-sm text-gray-600 mb-4 line-clamp-3">
              {book.description}
            </p>
          )}

          {/* Availability Status */}
          <div className="mb-4">
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
              book.available 
                ? 'bg-green-100 text-green-800' 
                : 'bg-gray-100 text-gray-800'
            }`}>
              {book.available ? 'Available' : 'Not Available'}
            </span>
          </div>

          {/* Owner Information */}
          {book.owner && (
            <div className="text-xs text-gray-500 mb-4">
              Listed by {book.owner.first_name} {book.owner.last_name}
            </div>
          )}

          {/* Action Buttons */}
          {showActions && (
            <div className="flex gap-2">
              {isOwner && showOwnerActions ? (
                // Owner actions
                <>
                  <button
                    onClick={handleEdit}
                    className="flex-1 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium py-2 px-4 rounded-md transition-colors"
                  >
                    Edit
                  </button>
                  <button
                    onClick={handleDelete}
                    className="flex-1 bg-red-600 hover:bg-red-700 text-white text-sm font-medium py-2 px-4 rounded-md transition-colors"
                  >
                    Delete
                  </button>
                </>
              ) : (
                // Non-owner actions
                !isOwner && book.available && (
                  <button
                    onClick={handleRequestExchange}
                    className="w-full bg-green-600 hover:bg-green-700 text-white text-sm font-medium py-2 px-4 rounded-md transition-colors"
                  >
                    Request Exchange
                  </button>
                )
              )}
            </div>
          )}
        </div>
      </div>

      {/* Exchange Request Form Modal */}
      {showExchangeForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-10 mx-auto p-5 border max-w-2xl shadow-lg rounded-md bg-white">
            <ExchangeRequestForm
              book={book}
              onSuccess={handleExchangeSuccess}
              onCancel={handleExchangeCancel}
              isOpen={true}
            />
          </div>
        </div>
      )}
    </>
  );
};

export default BookCard;