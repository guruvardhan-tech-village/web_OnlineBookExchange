import React, { useState, useEffect, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import SearchBar from './SearchBar';
import FilterPanel from './FilterPanel';
import BookList from './BookList';

const BookSearch = ({ 
  onBookSelect,
  onRequestExchange,
  showOwnerActions = false,
  onEdit,
  onDelete 
}) => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState({});
  const [isFilterPanelOpen, setIsFilterPanelOpen] = useState(false);

  // Initialize state from URL parameters
  useEffect(() => {
    const urlQuery = searchParams.get('q') || '';
    const urlFilters = {
      category: searchParams.get('category') || '',
      condition: searchParams.get('condition') || '',
      author: searchParams.get('author') || '',
      availability: searchParams.get('availability') || ''
    };

    // Remove empty filters
    const cleanFilters = Object.entries(urlFilters).reduce((acc, [key, value]) => {
      if (value && value.trim() !== '') {
        acc[key] = value;
      }
      return acc;
    }, {});

    setSearchQuery(urlQuery);
    setFilters(cleanFilters);

    // Open filter panel if there are active filters
    if (Object.keys(cleanFilters).length > 0) {
      setIsFilterPanelOpen(true);
    }
  }, [searchParams]);

  // Update URL parameters when search or filters change
  const updateUrlParams = useCallback((query, filterParams) => {
    const newParams = new URLSearchParams();
    
    if (query && query.trim()) {
      newParams.set('q', query.trim());
    }
    
    Object.entries(filterParams).forEach(([key, value]) => {
      if (value && value.trim() !== '') {
        newParams.set(key, value);
      }
    });

    setSearchParams(newParams);
  }, [setSearchParams]);

  // Handle search query change
  const handleSearch = useCallback((query) => {
    setSearchQuery(query);
    updateUrlParams(query, filters);
  }, [filters, updateUrlParams]);

  // Handle filters change
  const handleFiltersChange = useCallback((newFilters) => {
    setFilters(newFilters);
    updateUrlParams(searchQuery, newFilters);
  }, [searchQuery, updateUrlParams]);

  // Handle filter panel toggle
  const handleFilterToggle = (isOpen) => {
    setIsFilterPanelOpen(isOpen);
  };

  // Clear all search and filters
  const clearAll = () => {
    setSearchQuery('');
    setFilters({});
    setSearchParams(new URLSearchParams());
  };

  // Check if any search or filters are active
  const hasActiveSearchOrFilters = searchQuery.trim() !== '' || Object.keys(filters).length > 0;

  return (
    <div className="space-y-6">
      {/* Search and Filter Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="space-y-4">
          {/* Search Bar */}
          <div className="flex flex-col lg:flex-row lg:items-center lg:space-x-4 space-y-4 lg:space-y-0">
            <div className="flex-1">
              <SearchBar
                onSearch={handleSearch}
                initialValue={searchQuery}
                placeholder="Search books by title, author, or keyword..."
                showSuggestions={true}
                showHistory={true}
              />
            </div>
            
            {/* Filter Toggle Button (Mobile) */}
            <div className="lg:hidden">
              <button
                onClick={() => handleFilterToggle(!isFilterPanelOpen)}
                className="flex items-center justify-center w-full px-4 py-3 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                </svg>
                Filters
                {Object.keys(filters).length > 0 && (
                  <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {Object.keys(filters).length}
                  </span>
                )}
              </button>
            </div>
          </div>

          {/* Clear All Button */}
          {hasActiveSearchOrFilters && (
            <div className="flex justify-between items-center pt-4 border-t border-gray-200">
              <div className="text-sm text-gray-600">
                {searchQuery && (
                  <span>
                    Searching for: <strong>"{searchQuery}"</strong>
                  </span>
                )}
                {searchQuery && Object.keys(filters).length > 0 && <span> • </span>}
                {Object.keys(filters).length > 0 && (
                  <span>
                    {Object.keys(filters).length} filter{Object.keys(filters).length !== 1 ? 's' : ''} applied
                  </span>
                )}
              </div>
              <button
                onClick={clearAll}
                className="text-sm font-medium text-red-600 hover:text-red-700"
              >
                Clear All
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex flex-col lg:flex-row lg:space-x-6 space-y-6 lg:space-y-0">
        {/* Filter Panel - Desktop Sidebar */}
        <div className="hidden lg:block lg:w-80 flex-shrink-0">
          <div className="sticky top-6">
            <FilterPanel
              onFiltersChange={handleFiltersChange}
              initialFilters={filters}
              isOpen={true}
              showToggle={false}
            />
          </div>
        </div>

        {/* Filter Panel - Mobile Collapsible */}
        <div className="lg:hidden">
          <FilterPanel
            onFiltersChange={handleFiltersChange}
            initialFilters={filters}
            isOpen={isFilterPanelOpen}
            onToggle={handleFilterToggle}
            showToggle={true}
          />
        </div>

        {/* Book List */}
        <div className="flex-1 min-w-0">
          <BookList
            searchQuery={searchQuery}
            filters={filters}
            onBookSelect={onBookSelect}
            onRequestExchange={onRequestExchange}
            showOwnerActions={showOwnerActions}
            onEdit={onEdit}
            onDelete={onDelete}
          />
        </div>
      </div>
    </div>
  );
};

export default BookSearch;