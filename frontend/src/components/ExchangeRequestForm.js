import React, { useState } from 'react';
import { toast } from 'react-toastify';
import exchangeService from '../services/exchangeService';

const ExchangeRequestForm = ({ 
  book, 
  onSuccess, 
  onCancel, 
  isOpen = false,
  className = '' 
}) => {
  const [message, setMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!book) {
      toast.error('No book selected for exchange request');
      return;
    }

    setIsSubmitting(true);
    
    try {
      const exchangeData = {
        book_id: book.id,
        message: message.trim() || undefined
      };

      const response = await exchangeService.createExchange(exchangeData);
      
      toast.success('Exchange request sent successfully!');
      
      // Reset form
      setMessage('');
      setShowConfirmation(false);
      
      // Call success callback
      if (onSuccess) {
        onSuccess(response.exchange);
      }
      
    } catch (error) {
      toast.error(error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancel = () => {
    setMessage('');
    setShowConfirmation(false);
    if (onCancel) {
      onCancel();
    }
  };

  const handleRequestClick = () => {
    setShowConfirmation(true);
  };

  if (!isOpen && !showConfirmation) {
    return null;
  }

  return (
    <div className={`bg-white rounded-lg shadow-lg border border-gray-200 ${className}`}>
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900">
            Request Book Exchange
          </h3>
          <button
            onClick={handleCancel}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      {/* Book Information */}
      {book && (
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <div className="flex items-start space-x-4">
            {/* Book Image */}
            <div className="flex-shrink-0">
              {book.image_url ? (
                <img
                  src={book.image_url}
                  alt={`Cover of ${book.title}`}
                  className="w-16 h-20 object-cover rounded-md border border-gray-200"
                  onError={(e) => {
                    e.target.src = '/placeholder-book.png';
                  }}
                />
              ) : (
                <div className="w-16 h-20 bg-gray-200 rounded-md border border-gray-200 flex items-center justify-center">
                  <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </div>
              )}
            </div>

            {/* Book Details */}
            <div className="flex-1 min-w-0">
              <h4 className="text-sm font-medium text-gray-900 truncate">
                {book.title}
              </h4>
              <p className="text-sm text-gray-600 mt-1">
                by {book.author}
              </p>
              <div className="flex items-center gap-2 mt-2">
                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {book.category}
                </span>
                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  {book.condition}
                </span>
              </div>
              {book.owner && (
                <p className="text-xs text-gray-500 mt-2">
                  Owned by {book.owner.first_name} {book.owner.last_name}
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Form Content */}
      <form onSubmit={handleSubmit} className="px-6 py-4">
        {/* Message Input */}
        <div className="mb-6">
          <label htmlFor="exchange-message" className="block text-sm font-medium text-gray-700 mb-2">
            Message to Book Owner
            <span className="text-gray-500 font-normal ml-1">(Optional)</span>
          </label>
          <textarea
            id="exchange-message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Hi! I'm interested in exchanging books with you. I have some great titles that might interest you..."
            rows={4}
            maxLength={500}
            className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm resize-none"
          />
          <div className="flex justify-between items-center mt-1">
            <p className="text-xs text-gray-500">
              Add a personal message to increase your chances of a successful exchange
            </p>
            <span className="text-xs text-gray-400">
              {message.length}/500
            </span>
          </div>
        </div>

        {/* Exchange Guidelines */}
        <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
          <h5 className="text-sm font-medium text-blue-900 mb-2">
            Exchange Guidelines
          </h5>
          <ul className="text-xs text-blue-800 space-y-1">
            <li>• Be respectful and courteous in your communication</li>
            <li>• Clearly describe the condition of books you're offering</li>
            <li>• Arrange a safe meeting place for the exchange</li>
            <li>• Both parties should agree on the exchange terms</li>
          </ul>
        </div>

        {/* Confirmation Dialog */}
        {showConfirmation && (
          <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-md">
            <div className="flex items-start">
              <svg className="w-5 h-5 text-yellow-600 mt-0.5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
              <div>
                <h5 className="text-sm font-medium text-yellow-800">
                  Confirm Exchange Request
                </h5>
                <p className="text-sm text-yellow-700 mt-1">
                  Are you sure you want to send this exchange request? The book owner will be notified and can approve or decline your request.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex items-center justify-end space-x-3">
          <button
            type="button"
            onClick={handleCancel}
            disabled={isSubmitting}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Cancel
          </button>
          
          {!showConfirmation ? (
            <button
              type="button"
              onClick={handleRequestClick}
              disabled={isSubmitting || !book}
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Send Request
            </button>
          ) : (
            <button
              type="submit"
              disabled={isSubmitting || !book}
              className="px-4 py-2 text-sm font-medium text-white bg-green-600 border border-transparent rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center"
            >
              {isSubmitting ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Sending...
                </>
              ) : (
                'Confirm & Send'
              )}
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default ExchangeRequestForm;