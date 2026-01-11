import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import exchangeService from '../services/exchangeService';
import { useAuth } from '../contexts/AuthContext';

const ExchangeList = ({ 
  type = 'all', // 'all', 'sent', 'received'
  status = '', // '', 'pending', 'approved', 'rejected', 'completed'
  onExchangeUpdate,
  onExchangeSelect,
  className = ''
}) => {
  const { user } = useAuth();
  const [exchanges, setExchanges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 10,
    total: 0,
    pages: 0
  });
  const [selectedTab, setSelectedTab] = useState(type);
  const [selectedStatus, setSelectedStatus] = useState(status);

  // Fetch exchanges
  const fetchExchanges = async (page = 1) => {
    setLoading(true);
    setError(null);
    
    try {
      const params = {
        page,
        per_page: pagination.per_page,
        ...(selectedTab !== 'all' && { type: selectedTab }),
        ...(selectedStatus && { status: selectedStatus })
      };

      const response = await exchangeService.getExchanges(params);
      
      setExchanges(response.exchanges || []);
      setPagination(response.pagination || {
        page: 1,
        per_page: 10,
        total: 0,
        pages: 0
      });
    } catch (err) {
      setError(err.message);
      setExchanges([]);
    } finally {
      setLoading(false);
    }
  };

  // Fetch exchanges when component mounts or filters change
  useEffect(() => {
    fetchExchanges(1);
  }, [selectedTab, selectedStatus]); // eslint-disable-line react-hooks/exhaustive-deps

  // Handle page change
  const handlePageChange = (newPage) => {
    if (newPage >= 1 && newPage <= pagination.pages) {
      fetchExchanges(newPage);
    }
  };

  // Handle tab change
  const handleTabChange = (tab) => {
    setSelectedTab(tab);
  };

  // Handle status filter change
  const handleStatusChange = (status) => {
    setSelectedStatus(status);
  };

  // Handle exchange action (approve, reject, complete, cancel)
  const handleExchangeAction = async (exchange, action, message = '') => {
    try {
      let response;
      
      switch (action) {
        case 'approve':
          response = await exchangeService.approveExchange(exchange.id, message);
          toast.success('Exchange request approved!');
          break;
        case 'reject':
          response = await exchangeService.rejectExchange(exchange.id, message);
          toast.success('Exchange request rejected');
          break;
        case 'complete':
          response = await exchangeService.completeExchange(exchange.id, message);
          toast.success('Exchange marked as completed!');
          break;
        case 'cancel':
          response = await exchangeService.cancelExchange(exchange.id);
          toast.success('Exchange request cancelled');
          break;
        default:
          throw new Error('Invalid action');
      }

      // Refresh the list
      fetchExchanges(pagination.page);
      
      // Call update callback
      if (onExchangeUpdate) {
        onExchangeUpdate(response.exchange || exchange, action);
      }
      
    } catch (error) {
      toast.error(error.message);
    }
  };

  // Get status badge color
  const getStatusBadgeColor = (status) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'approved':
        return 'bg-green-100 text-green-800';
      case 'rejected':
        return 'bg-red-100 text-red-800';
      case 'completed':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
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

  // Render exchange item
  const renderExchangeItem = (exchange) => {
    const isRequester = exchange.requester_id === user?.id;
    const isOwner = exchange.owner_id === user?.id;
    const otherUser = isRequester ? exchange.owner : exchange.requester;
    const book = exchange.book;

    return (
      <div
        key={exchange.id}
        className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer"
        onClick={() => onExchangeSelect && onExchangeSelect(exchange)}
      >
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0">
              <div className={`w-3 h-3 rounded-full ${
                exchange.status === 'pending' ? 'bg-yellow-400' :
                exchange.status === 'approved' ? 'bg-green-400' :
                exchange.status === 'rejected' ? 'bg-red-400' :
                exchange.status === 'completed' ? 'bg-blue-400' : 'bg-gray-400'
              }`}></div>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-900">
                {isRequester ? 'Request Sent' : 'Request Received'}
              </h3>
              <p className="text-xs text-gray-500">
                {formatDate(exchange.created_at)}
              </p>
            </div>
          </div>
          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusBadgeColor(exchange.status)}`}>
            {exchange.status.charAt(0).toUpperCase() + exchange.status.slice(1)}
          </span>
        </div>

        {/* Book and User Info */}
        <div className="flex items-start space-x-4 mb-4">
          {/* Book Image */}
          <div className="flex-shrink-0">
            {book?.image_url ? (
              <img
                src={book.image_url}
                alt={`Cover of ${book?.title}`}
                className="w-12 h-16 object-cover rounded border border-gray-200"
                onError={(e) => {
                  e.target.src = '/placeholder-book.png';
                }}
              />
            ) : (
              <div className="w-12 h-16 bg-gray-200 rounded border border-gray-200 flex items-center justify-center">
                <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
            )}
          </div>

          {/* Details */}
          <div className="flex-1 min-w-0">
            <h4 className="text-sm font-medium text-gray-900 truncate">
              {book?.title || 'Unknown Book'}
            </h4>
            <p className="text-sm text-gray-600">
              by {book?.author || 'Unknown Author'}
            </p>
            <p className="text-sm text-gray-600 mt-1">
              {isRequester ? 'From' : 'To'}: {otherUser?.first_name} {otherUser?.last_name}
            </p>
            {book && (
              <div className="flex items-center gap-2 mt-2">
                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {book.category}
                </span>
                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  {book.condition}
                </span>
              </div>
            )}
          </div>
        </div>

        {/* Message */}
        {exchange.message && (
          <div className="mb-4 p-3 bg-gray-50 rounded-md">
            <p className="text-sm text-gray-700">
              "{exchange.message}"
            </p>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex items-center justify-between">
          <div className="text-xs text-gray-500">
            ID: #{exchange.id}
          </div>
          
          <div className="flex items-center space-x-2">
            {/* Owner actions for pending requests */}
            {isOwner && exchange.status === 'pending' && (
              <>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleExchangeAction(exchange, 'approve');
                  }}
                  className="px-3 py-1 text-xs font-medium text-green-700 bg-green-100 rounded-md hover:bg-green-200 transition-colors"
                >
                  Approve
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleExchangeAction(exchange, 'reject');
                  }}
                  className="px-3 py-1 text-xs font-medium text-red-700 bg-red-100 rounded-md hover:bg-red-200 transition-colors"
                >
                  Reject
                </button>
              </>
            )}

            {/* Complete action for approved exchanges */}
            {exchange.status === 'approved' && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleExchangeAction(exchange, 'complete');
                }}
                className="px-3 py-1 text-xs font-medium text-blue-700 bg-blue-100 rounded-md hover:bg-blue-200 transition-colors"
              >
                Mark Complete
              </button>
            )}

            {/* Cancel action for requester on pending requests */}
            {isRequester && exchange.status === 'pending' && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleExchangeAction(exchange, 'cancel');
                }}
                className="px-3 py-1 text-xs font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
              >
                Cancel
              </button>
            )}

            {/* View details button */}
            <button
              onClick={(e) => {
                e.stopPropagation();
                if (onExchangeSelect) onExchangeSelect(exchange);
              }}
              className="px-3 py-1 text-xs font-medium text-blue-700 bg-blue-100 rounded-md hover:bg-blue-200 transition-colors"
            >
              Details
            </button>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header and Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
          {/* Title */}
          <h2 className="text-xl font-semibold text-gray-900">
            Exchange Requests
          </h2>

          {/* Filters */}
          <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-4">
            {/* Type Filter */}
            <div className="flex rounded-md shadow-sm">
              <button
                onClick={() => handleTabChange('all')}
                className={`px-4 py-2 text-sm font-medium rounded-l-md border ${
                  selectedTab === 'all'
                    ? 'bg-blue-600 text-white border-blue-600'
                    : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                }`}
              >
                All
              </button>
              <button
                onClick={() => handleTabChange('sent')}
                className={`px-4 py-2 text-sm font-medium border-t border-b ${
                  selectedTab === 'sent'
                    ? 'bg-blue-600 text-white border-blue-600'
                    : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                }`}
              >
                Sent
              </button>
              <button
                onClick={() => handleTabChange('received')}
                className={`px-4 py-2 text-sm font-medium rounded-r-md border ${
                  selectedTab === 'received'
                    ? 'bg-blue-600 text-white border-blue-600'
                    : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                }`}
              >
                Received
              </button>
            </div>

            {/* Status Filter */}
            <select
              value={selectedStatus}
              onChange={(e) => handleStatusChange(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">All Status</option>
              <option value="pending">Pending</option>
              <option value="approved">Approved</option>
              <option value="rejected">Rejected</option>
              <option value="completed">Completed</option>
            </select>
          </div>
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="space-y-4">
          {[...Array(3)].map((_, index) => (
            <div key={index} className="bg-white border border-gray-200 rounded-lg p-6 animate-pulse">
              <div className="flex items-start space-x-4">
                <div className="w-12 h-16 bg-gray-200 rounded"></div>
                <div className="flex-1 space-y-2">
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                  <div className="h-3 bg-gray-200 rounded w-2/3"></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-6">
          <div className="flex items-center">
            <svg className="w-5 h-5 text-red-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <h3 className="text-sm font-medium text-red-800">Error Loading Exchanges</h3>
              <p className="text-sm text-red-700 mt-1">{error}</p>
            </div>
          </div>
          <button
            onClick={() => fetchExchanges(pagination.page)}
            className="mt-3 text-sm font-medium text-red-600 hover:text-red-700"
          >
            Try Again
          </button>
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && exchanges.length === 0 && (
        <div className="text-center py-12">
          <div className="max-w-md mx-auto">
            <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
            </svg>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No Exchange Requests</h3>
            <p className="text-gray-600">
              {selectedTab === 'sent' 
                ? "You haven't sent any exchange requests yet."
                : selectedTab === 'received'
                ? "You haven't received any exchange requests yet."
                : "No exchange requests found."}
            </p>
          </div>
        </div>
      )}

      {/* Exchange List */}
      {!loading && !error && exchanges.length > 0 && (
        <div className="space-y-4">
          {exchanges.map(renderExchangeItem)}
        </div>
      )}

      {/* Pagination */}
      {!loading && !error && pagination.pages > 1 && (
        <div className="flex items-center justify-center space-x-2 pt-6">
          <button
            onClick={() => handlePageChange(pagination.page - 1)}
            disabled={pagination.page <= 1}
            className={`px-3 py-2 text-sm font-medium rounded-md ${
              pagination.page <= 1
                ? 'text-gray-400 cursor-not-allowed'
                : 'text-gray-700 hover:text-blue-600 hover:bg-blue-50'
            }`}
          >
            Previous
          </button>

          <div className="flex space-x-1">
            {[...Array(pagination.pages)].map((_, index) => {
              const pageNum = index + 1;
              const isCurrentPage = pageNum === pagination.page;
              
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
                : 'text-gray-700 hover:text-blue-600 hover:bg-blue-50'
            }`}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default ExchangeList;