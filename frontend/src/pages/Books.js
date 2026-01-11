import React from 'react';
import BookSearch from '../components/BookSearch';
import { toast } from 'react-toastify';

const Books = () => {
  const handleBookSelect = (book) => {
    // You could navigate to a book detail page here
    console.log('Selected book:', book);
  };

  const handleRequestExchange = (book) => {
    // Navigate to exchange request page or show modal
    toast.info(`Exchange request for "${book.title}" - Feature coming soon!`);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Browse Books</h1>
          <p className="mt-2 text-gray-600">
            Discover and exchange books with other readers in our community.
          </p>
        </div>

        {/* Book Search and Listing */}
        <BookSearch
          onBookSelect={handleBookSelect}
          onRequestExchange={handleRequestExchange}
          showOwnerActions={false}
        />
      </div>
    </div>
  );
};

export default Books;