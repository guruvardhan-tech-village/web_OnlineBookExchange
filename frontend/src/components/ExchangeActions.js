import React, { useState } from 'react';
import { toast } from 'react-toastify';
import exchangeService from '../services/exchangeService';
import { useAuth } from '../contexts/AuthContext';

const ExchangeActions = ({ 
  exchange, 
  onActionComplete,
  showHistory = false,
  className = '' 
}) => {
  const { user } = useAuth();
  const [isProcessing, setIsProcessing] = useState(false);
  const [showMessageModal, setShowMessageModal] = useState(false);
  const [actionType, setActionType] = useState('');
  const [message, setMessage] = useState('');
  const [history, setHistory] = useState(null);
  const [loadingHistory, setLoadingHistory] = useState(false);

  if (!exchange || !user) {
    return null;
  }

  const isRequester = exchange.requester_id === user.id;
  const isOwner = exchange.owner_id === user.id;

  // Handle action with optional message
  const handleActionWithMessage = (action) => {
    setActionType(action);
    setMessage('');
    setShowMessageModal(true);
  };

  // Handle direct action (no message required)
  const handleDirectAction = async (action) => {
    await executeAction(action, '');
  };

  // Execute the action
  const executeAction = async (action, actionMessage = '') => {
    setIsProcessing(true);
    
    try {
      let response;
      let successMessage = '';

      switch (action) {
        case 'approve':
          response = await exchangeService.approveExchange(exchange.id, actionMessage);
          successMessage = 'Exchange request approved successfully!';
          break;
        case 'reject':
          response = await exchangeService.rejectExchange(exchange.id, actionMessage);
          successMessage = 'Exchange request rejected';
          break;
        case 'complete':
          response = await exchangeService.completeExchange(exchange.id, actionMessage);
          successMessage = 'Exchange marked as completed!';
          break;
        case 'cancel':
          response = await exchangeService.cancelExchange(exchange.id);
          successMessage = 'Exchange request cancelled';
          break;
        default:
          throw new Error('Invalid action');
      }

      toast.success(successMessage);
      
      // Close modal and reset state
      setShowMessageModal(false);
      setActionType('');
      setMessage('');
      
      // Call completion callback
      if (onActionComplete) {
        onActionComplete(response.exchange || exchange, action);
      }
      
    } catch (error) {
      toast.error(error.message);
    } finally {
      setIsProcessing(false);
    }
  };

  // Handle message modal submit
  const handleMessageSubmit = (e) => {
    e.preventDefault();
    executeAction(actionType, message.trim());
  };

  // Load exchange history
  const loadHistory = async () => {
    if (history) {
      setHistory(null);
      return;
    }

    setLoadingHistory(true);
    try {
      const response = await exchangeService.getExchangeHistory(exchange.id);
      setHistory(response.history);
    } catch (error) {
      toast.error('Failed to load exchange history');
    } finally {
      setLoadingHistory(false);
    }
  };

  // Get status color
  const getStatusColor = (status) => {
    switch (status) {
      case 'pending':
        return 'text-yellow-600 bg-yellow-100';
      case 'approved':
        return 'text-green-600 bg-green-100';
      case 'rejected':
        return 'text-red-600 bg-red-100';
      case 'completed':
        return 'text-blue-600 bg-blue-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  // Format date
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className={`bg-white rounded-lg border border-gray-200 ${className}`}>
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900">
            Exchange Actions
          </h3>
          <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(exchange.status)}`}>
            {exchange.status.charAt(0).toUpperCase() + exchange.status.slice(1)}
          </span>
        </div>
      </div>

      {/* Exchange Info */}
      <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <span className="font-medium text-gray-700">Request ID:</span>
            <span className="ml-2 text-gray-900">#{exchange.id}</span>
          </div>
          <div>
            <span className="font-medium text-gray-700">Created:</span>
            <span className="ml-2 text-gray-900">{formatDate(exchange.created_at)}</span>
          </div>
          <div>
            <span className="font-medium text-gray-700">Book:</span>
            <span className="ml-2 text-gray-900">{exchange.book?.title || 'Unknown'}</span>
          </div>
          <div>
            <span className="font-medium text-gray-700">
              {isRequester ? 'Book Owner:' : 'Requester:'}
            </span>
            <span className="ml-2 text-gray-900">
              {isRequester 
                ? `${exchange.owner?.first_name} ${exchange.owner?.last_name}`
                : `${exchange.requester?.first_name} ${exchange.requester?.last_name}`
              }
            </span>
          </div>
        </div>
        
        {exchange.message && (
          <div className="mt-4 p-3 bg-white rounded-md border border-gray-200">
            <p className="text-sm text-gray-700">
              <span className="font-medium">Message:</span> "{exchange.message}"
            </p>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="px-6 py-4">
        <div className="flex flex-wrap gap-3">
          {/* Owner actions for pending requests */}
          {isOwner && exchange.status === 'pending' && (
            <>
              <button
                onClick={() => handleActionWithMessage('approve')}
                disabled={isProcessing}
                className="flex items-center px-4 py-2 text-sm font-medium text-white bg-green-600 border border-transparent rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Approve Request
              </button>
              <button
                onClick={() => handleActionWithMessage('reject')}
                disabled={isProcessing}
                className="flex items-center px-4 py-2 text-sm font-medium text-red-700 bg-red-100 border border-red-300 rounded-md hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
                Reject Request
              </button>
            </>
          )}

          {/* Complete action for approved exchanges */}
          {exchange.status === 'approved' && (
            <button
              onClick={() => handleActionWithMessage('complete')}
              disabled={isProcessing}
              className="flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Mark as Complete
            </button>
          )}

          {/* Cancel action for requester on pending requests */}
          {isRequester && exchange.status === 'pending' && (
            <button
              onClick={() => handleDirectAction('cancel')}
              disabled={isProcessing}
              className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
              Cancel Request
            </button>
          )}

          {/* History toggle button */}
          {showHistory && (
            <button
              onClick={loadHistory}
              disabled={loadingHistory}
              className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {loadingHistory ? 'Loading...' : history ? 'Hide History' : 'Show History'}
            </button>
          )}
        </div>

        {/* Processing indicator */}
        {isProcessing && (
          <div className="mt-4 flex items-center text-sm text-gray-600">
            <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-gray-600" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Processing action...
          </div>
        )}
      </div>

      {/* History Section */}
      {history && (
        <div className="px-6 py-4 border-t border-gray-200 bg-gray-50">
          <h4 className="text-sm font-medium text-gray-900 mb-3">Exchange History</h4>
          <div className="space-y-3">
            {history.timeline?.map((event, index) => (
              <div key={index} className="flex items-start space-x-3">
                <div className={`flex-shrink-0 w-2 h-2 rounded-full mt-2 ${
                  event.status === 'pending' ? 'bg-yellow-400' :
                  event.status === 'approved' ? 'bg-green-400' :
                  event.status === 'rejected' ? 'bg-red-400' :
                  event.status === 'completed' ? 'bg-blue-400' : 'bg-gray-400'
                }`}></div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-900">{event.description}</p>
                  <p className="text-xs text-gray-500">{formatDate(event.timestamp)}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Message Modal */}
      {showMessageModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                {actionType === 'approve' ? 'Approve Exchange Request' :
                 actionType === 'reject' ? 'Reject Exchange Request' :
                 actionType === 'complete' ? 'Complete Exchange' : 'Add Message'}
              </h3>
              
              <form onSubmit={handleMessageSubmit}>
                <div className="mb-4">
                  <label htmlFor="action-message" className="block text-sm font-medium text-gray-700 mb-2">
                    Message {actionType === 'approve' || actionType === 'complete' ? '(Optional)' : '(Recommended)'}
                  </label>
                  <textarea
                    id="action-message"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder={
                      actionType === 'approve' ? 'Let them know you\'re excited about the exchange...' :
                      actionType === 'reject' ? 'Explain why you\'re declining this request...' :
                      actionType === 'complete' ? 'Share how the exchange went...' : 'Add a message...'
                    }
                    rows={3}
                    maxLength={500}
                    className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm resize-none"
                  />
                  <div className="text-right mt-1">
                    <span className="text-xs text-gray-400">{message.length}/500</span>
                  </div>
                </div>

                <div className="flex items-center justify-end space-x-3">
                  <button
                    type="button"
                    onClick={() => setShowMessageModal(false)}
                    disabled={isProcessing}
                    className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={isProcessing}
                    className={`px-4 py-2 text-sm font-medium text-white border border-transparent rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors ${
                      actionType === 'approve' ? 'bg-green-600 hover:bg-green-700 focus:ring-green-500' :
                      actionType === 'reject' ? 'bg-red-600 hover:bg-red-700 focus:ring-red-500' :
                      actionType === 'complete' ? 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500' :
                      'bg-gray-600 hover:bg-gray-700 focus:ring-gray-500'
                    }`}
                  >
                    {isProcessing ? 'Processing...' : 
                     actionType === 'approve' ? 'Approve' :
                     actionType === 'reject' ? 'Reject' :
                     actionType === 'complete' ? 'Complete' : 'Submit'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ExchangeActions;