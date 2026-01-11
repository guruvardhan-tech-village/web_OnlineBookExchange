import React, { useState, useEffect } from 'react';

const FilterPanel = ({ 
  onFiltersChange, 
  initialFilters = {},
  isOpen = false,
  onToggle,
  showToggle = true 
}) => {
  const [filters, setFilters] = useState({
    category: '',
    condition: '',
    author: '',
    availability: '',
    ...initialFilters
  });

  const [isExpanded, setIsExpanded] = useState(isOpen);

  // Predefined filter options
  const categories = [
    'Fiction',
    'Non-Fiction',
    'Mystery',
    'Romance',
    'Science Fiction',
    'Fantasy',
    'Biography',
    'History',
    'Self-Help',
    'Technology',
    'Business',
    'Health',
    'Travel',
    'Cooking',
    'Art',
    'Education',
    'Children',
    'Young Adult'
  ];

  const conditions = [
    { value: 'new', label: 'New' },
    { value: 'like_new', label: 'Like New' },
    { value: 'good', label: 'Good' },
    { value: 'fair', label: 'Fair' },
    { value: 'poor', label: 'Poor' }
  ];

  const availabilityOptions = [
    { value: 'available', label: 'Available' },
    { value: 'unavailable', label: 'Not Available' }
  ];

  // Update filters when initialFilters change
  useEffect(() => {
    setFilters(prev => ({
      ...prev,
      ...initialFilters
    }));
  }, [initialFilters]);

  // Handle filter change
  const handleFilterChange = (filterType, value) => {
    const newFilters = {
      ...filters,
      [filterType]: value
    };
    
    setFilters(newFilters);
    
    // Remove empty filters before passing to parent
    const cleanFilters = Object.entries(newFilters).reduce((acc, [key, val]) => {
      if (val && val.trim() !== '') {
        acc[key] = val;
      }
      return acc;
    }, {});
    
    if (onFiltersChange) {
      onFiltersChange(cleanFilters);
    }
  };

  // Clear all filters
  const clearAllFilters = () => {
    const clearedFilters = {
      category: '',
      condition: '',
      author: '',
      availability: ''
    };
    
    setFilters(clearedFilters);
    
    if (onFiltersChange) {
      onFiltersChange({});
    }
  };

  // Check if any filters are active
  const hasActiveFilters = Object.values(filters).some(value => value && value.trim() !== '');

  // Toggle panel expansion
  const toggleExpanded = () => {
    const newExpanded = !isExpanded;
    setIsExpanded(newExpanded);
    if (onToggle) {
      onToggle(newExpanded);
    }
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
      {/* Filter Header */}
      {showToggle && (
        <div className="px-4 py-3 border-b border-gray-200">
          <button
            onClick={toggleExpanded}
            className="flex items-center justify-between w-full text-left"
          >
            <div className="flex items-center">
              <h3 className="text-lg font-medium text-gray-900">Filters</h3>
              {hasActiveFilters && (
                <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {Object.values(filters).filter(v => v && v.trim() !== '').length}
                </span>
              )}
            </div>
            <svg
              className={`h-5 w-5 text-gray-400 transform transition-transform ${
                isExpanded ? 'rotate-180' : ''
              }`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </button>
        </div>
      )}

      {/* Filter Content */}
      {(isExpanded || !showToggle) && (
        <div className="p-4 space-y-6">
          {/* Category Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Category
            </label>
            <select
              value={filters.category}
              onChange={(e) => handleFilterChange('category', e.target.value)}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
            >
              <option value="">All Categories</option>
              {categories.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>
          </div>

          {/* Condition Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Condition
            </label>
            <select
              value={filters.condition}
              onChange={(e) => handleFilterChange('condition', e.target.value)}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
            >
              <option value="">All Conditions</option>
              {conditions.map((condition) => (
                <option key={condition.value} value={condition.value}>
                  {condition.label}
                </option>
              ))}
            </select>
          </div>

          {/* Author Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Author
            </label>
            <input
              type="text"
              value={filters.author}
              onChange={(e) => handleFilterChange('author', e.target.value)}
              placeholder="Enter author name..."
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
            />
          </div>

          {/* Availability Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Availability
            </label>
            <select
              value={filters.availability}
              onChange={(e) => handleFilterChange('availability', e.target.value)}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
            >
              <option value="">All Books</option>
              {availabilityOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          {/* Filter Actions */}
          <div className="flex items-center justify-between pt-4 border-t border-gray-200">
            <button
              onClick={clearAllFilters}
              disabled={!hasActiveFilters}
              className={`text-sm font-medium ${
                hasActiveFilters
                  ? 'text-red-600 hover:text-red-700'
                  : 'text-gray-400 cursor-not-allowed'
              }`}
            >
              Clear All
            </button>
            
            <div className="text-xs text-gray-500">
              {hasActiveFilters ? (
                `${Object.values(filters).filter(v => v && v.trim() !== '').length} filter${
                  Object.values(filters).filter(v => v && v.trim() !== '').length !== 1 ? 's' : ''
                } active`
              ) : (
                'No filters applied'
              )}
            </div>
          </div>
        </div>
      )}

      {/* Mobile Filter Summary (when collapsed) */}
      {showToggle && !isExpanded && hasActiveFilters && (
        <div className="px-4 py-2 bg-gray-50 rounded-b-lg">
          <div className="flex flex-wrap gap-2">
            {filters.category && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                {filters.category}
                <button
                  onClick={() => handleFilterChange('category', '')}
                  className="ml-1 text-blue-600 hover:text-blue-800"
                >
                  ×
                </button>
              </span>
            )}
            {filters.condition && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                {conditions.find(c => c.value === filters.condition)?.label}
                <button
                  onClick={() => handleFilterChange('condition', '')}
                  className="ml-1 text-green-600 hover:text-green-800"
                >
                  ×
                </button>
              </span>
            )}
            {filters.author && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                Author: {filters.author}
                <button
                  onClick={() => handleFilterChange('author', '')}
                  className="ml-1 text-purple-600 hover:text-purple-800"
                >
                  ×
                </button>
              </span>
            )}
            {filters.availability && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                {availabilityOptions.find(a => a.value === filters.availability)?.label}
                <button
                  onClick={() => handleFilterChange('availability', '')}
                  className="ml-1 text-yellow-600 hover:text-yellow-800"
                >
                  ×
                </button>
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default FilterPanel;