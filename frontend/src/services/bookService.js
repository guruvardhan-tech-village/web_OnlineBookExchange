import api from './api';

const bookService = {
  async getBooks(params = {}) {
    try {
      const response = await api.get('/books', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch books');
    }
  },

  async getBook(id) {
    try {
      const response = await api.get(`/books/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch book');
    }
  },

  async createBook(bookData) {
    try {
      const response = await api.post('/books', bookData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to create book');
    }
  },

  async updateBook(id, bookData) {
    try {
      const response = await api.put(`/books/${id}`, bookData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to update book');
    }
  },

  async deleteBook(id) {
    try {
      await api.delete(`/books/${id}`);
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to delete book');
    }
  },

  async uploadImage(file) {
    try {
      const formData = new FormData();
      formData.append('image', file);
      
      const response = await api.post('/books/upload-image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to upload image');
    }
  },

  async searchBooks(query, filters = {}) {
    try {
      const params = { 
        q: query, 
        ...filters,
        // Map frontend filter names to backend expected names
        ...(filters.category && { category: filters.category }),
        ...(filters.condition && { condition: filters.condition }),
        ...(filters.author && { author: filters.author }),
        ...(filters.availability && { 
          available: filters.availability === 'available' ? true : 
                    filters.availability === 'unavailable' ? false : undefined 
        })
      };
      
      // Remove undefined values
      Object.keys(params).forEach(key => {
        if (params[key] === undefined) {
          delete params[key];
        }
      });
      
      const response = await api.get('/books/search', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to search books');
    }
  }
};

export default bookService;