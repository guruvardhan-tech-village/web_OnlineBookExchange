import api from './api';

const adminService = {
  // Get system statistics for admin dashboard
  getStats: async () => {
    try {
      const response = await api.get('/admin/stats');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Get all users with pagination and search
  getUsers: async (params = {}) => {
    try {
      const response = await api.get('/admin/users', { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Update user role
  updateUserRole: async (userId, role) => {
    try {
      const response = await api.put(`/admin/users/${userId}/role`, { role });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Get books pending moderation
  getPendingBooks: async (params = {}) => {
    try {
      const response = await api.get('/admin/books/pending', { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Moderate book listing
  moderateBook: async (bookId, action, reason = '') => {
    try {
      const response = await api.put(`/admin/books/${bookId}/moderate`, {
        action,
        reason
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  }
};

export default adminService;