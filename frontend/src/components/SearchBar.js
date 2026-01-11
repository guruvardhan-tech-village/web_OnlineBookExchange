import React, { useState, useEffect, useRef } from 'react';
import { debounce } from 'lodash';
import useInteractionTracking from '../hooks/useInteractionTracking';

const SearchBar = ({ 
  onSearch, 
  placeholder = "Search books by title, author, or keyword...",
  initialValue = "",
  showSuggestions = true,
  showHistory = true 
}) => {
  const [query, setQuery] = useState(initialValue);
  const [suggestions, setSuggestions] = useState([]);
  const [searchHistory, setSearchHistory] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  
  const { trackSearch } = useInteractionTracking();
  const inputRef = useRef(null);
  const dropdownRef = useRef(null);

  // Load search history from localStorage on component mount
  useEffect(() => {
    const savedHistory = localStorage.getItem('bookSearchHistory');
    if (savedHistory) {
      try {
        setSearchHistory(JSON.parse(savedHistory));
      } catch (error) {
        console.error('Failed to parse search history:', error);
      }
    }
  }, []);

  // Debounced search function
  const debouncedSearch = useRef(
    debounce((searchQuery) => {
      if (onSearch) {
        onSearch(searchQuery);
      }
    }, 300)
  ).current;

  // Handle input change
  const handleInputChange = (e) => {
    const value = e.target.value;
    setQuery(value);
    setSelectedIndex(-1);

    if (value.trim()) {
      setShowDropdown(true);
      if (showSuggestions) {
        fetchSuggestions(value);
      }
      debouncedSearch(value);
    } else {
      setShowDropdown(false);
      setSuggestions([]);
      debouncedSearch('');
    }
  };

  // Fetch search suggestions (mock implementation - replace with actual API call)
  const fetchSuggestions = async (searchQuery) => {
    if (!searchQuery.trim()) {
      setSuggestions([]);
      return;
    }

    setIsLoading(true);
    try {
      // Mock suggestions based on common book-related terms
      const mockSuggestions = [
        `${searchQuery} - Fiction`,
        `${searchQuery} - Non-fiction`,
        `${searchQuery} - Mystery`,
        `${searchQuery} - Romance`,
        `${searchQuery} - Science Fiction`
      ].filter(suggestion => 
        suggestion.toLowerCase().includes(searchQuery.toLowerCase())
      ).slice(0, 5);

      setSuggestions(mockSuggestions);
    } catch (error) {
      console.error('Failed to fetch suggestions:', error);
      setSuggestions([]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle search submission
  const handleSearch = (searchQuery = query) => {
    const trimmedQuery = searchQuery.trim();
    if (!trimmedQuery) return;

    // Track search interaction
    trackSearch(trimmedQuery);

    // Add to search history
    addToSearchHistory(trimmedQuery);
    
    // Close dropdown
    setShowDropdown(false);
    
    // Trigger search
    if (onSearch) {
      onSearch(trimmedQuery);
    }
  };

  // Add search term to history
  const addToSearchHistory = (searchTerm) => {
    const updatedHistory = [
      searchTerm,
      ...searchHistory.filter(item => item !== searchTerm)
    ].slice(0, 10); // Keep only last 10 searches

    setSearchHistory(updatedHistory);
    localStorage.setItem('bookSearchHistory', JSON.stringify(updatedHistory));
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    handleSearch();
  };

  // Handle suggestion/history item click
  const handleItemClick = (item) => {
    setQuery(item);
    handleSearch(item);
  };

  // Handle keyboard navigation
  const handleKeyDown = (e) => {
    const items = [...suggestions, ...searchHistory];
    
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev => 
          prev < items.length - 1 ? prev + 1 : prev
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev => prev > -1 ? prev - 1 : -1);
        break;
      case 'Enter':
        e.preventDefault();
        if (selectedIndex >= 0 && items[selectedIndex]) {
          handleItemClick(items[selectedIndex]);
        } else {
          handleSearch();
        }
        break;
      case 'Escape':
        setShowDropdown(false);
        setSelectedIndex(-1);
        inputRef.current?.blur();
        break;
      default:
        break;
    }
  };

  // Handle input focus
  const handleFocus = () => {
    if (query.trim() || searchHistory.length > 0) {
      setShowDropdown(true);
    }
  };

  // Handle click outside to close dropdown
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        dropdownRef.current && 
        !dropdownRef.current.contains(event.target) &&
        !inputRef.current?.contains(event.target)
      ) {
        setShowDropdown(false);
        setSelectedIndex(-1);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Clear search history
  const clearHistory = () => {
    setSearchHistory([]);
    localStorage.removeItem('bookSearchHistory');
  };

  // Clear current search
  const clearSearch = () => {
    setQuery('');
    setShowDropdown(false);
    setSuggestions([]);
    if (onSearch) {
      onSearch('');
    }
  };

  const combinedItems = [
    ...suggestions.map(item => ({ text: item, type: 'suggestion' })),
    ...(showHistory && searchHistory.length > 0 ? 
      searchHistory.map(item => ({ text: item, type: 'history' })) : [])
  ];

  return (
    <div className="relative w-full max-w-2xl">
      <form onSubmit={handleSubmit} className="relative">
        {/* Search Input */}
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg
              className="h-5 w-5 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
          
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            onFocus={handleFocus}
            placeholder={placeholder}
            className="block w-full pl-10 pr-12 py-3 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
          />
          
          {/* Clear Button */}
          {query && (
            <button
              type="button"
              onClick={clearSearch}
              className="absolute inset-y-0 right-0 pr-3 flex items-center"
            >
              <svg
                className="h-5 w-5 text-gray-400 hover:text-gray-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          )}
        </div>
      </form>

      {/* Dropdown with Suggestions and History */}
      {showDropdown && (combinedItems.length > 0 || isLoading) && (
        <div
          ref={dropdownRef}
          className="absolute z-50 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-80 overflow-y-auto"
        >
          {isLoading && (
            <div className="px-4 py-3 text-sm text-gray-500 flex items-center">
              <svg className="animate-spin -ml-1 mr-3 h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Loading suggestions...
            </div>
          )}

          {/* Suggestions Section */}
          {suggestions.length > 0 && (
            <div>
              <div className="px-4 py-2 text-xs font-medium text-gray-500 uppercase tracking-wide bg-gray-50 border-b">
                Suggestions
              </div>
              {suggestions.map((suggestion, index) => (
                <button
                  key={`suggestion-${index}`}
                  onClick={() => handleItemClick(suggestion)}
                  className={`w-full text-left px-4 py-3 text-sm hover:bg-gray-50 flex items-center ${
                    selectedIndex === index ? 'bg-blue-50 text-blue-700' : 'text-gray-900'
                  }`}
                >
                  <svg className="h-4 w-4 mr-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  {suggestion}
                </button>
              ))}
            </div>
          )}

          {/* Search History Section */}
          {showHistory && searchHistory.length > 0 && (
            <div>
              <div className="px-4 py-2 text-xs font-medium text-gray-500 uppercase tracking-wide bg-gray-50 border-b flex items-center justify-between">
                <span>Recent Searches</span>
                <button
                  onClick={clearHistory}
                  className="text-xs text-blue-600 hover:text-blue-700 font-normal"
                >
                  Clear
                </button>
              </div>
              {searchHistory.map((historyItem, index) => {
                const adjustedIndex = suggestions.length + index;
                return (
                  <button
                    key={`history-${index}`}
                    onClick={() => handleItemClick(historyItem)}
                    className={`w-full text-left px-4 py-3 text-sm hover:bg-gray-50 flex items-center ${
                      selectedIndex === adjustedIndex ? 'bg-blue-50 text-blue-700' : 'text-gray-900'
                    }`}
                  >
                    <svg className="h-4 w-4 mr-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {historyItem}
                  </button>
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SearchBar;