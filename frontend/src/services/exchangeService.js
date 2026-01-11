import api from './api';

const exchangeService = {
  async getExchanges(params = {}) {
    try {
      const response = await api.get('/exchanges', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch exchanges');
    }
  },

  async createExchange(exchangeData) {
    try {
      const response = await api.post('/exchanges', exchangeData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to create exchange request');
    }
  },

  async updateExchange(exchangeId, updateData) {
    try {
      const response = await api.put(`/exchanges/${exchangeId}`, updateData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to update exchange request');
    }
  },

  async getExchangeHistory(exchangeId) {
    try {
      const response = await api.get(`/exchanges/${exchangeId}/history`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch exchange history');
    }
  },

  async cancelExchange(exchangeId) {
    try {
      const response = await api.delete(`/exchanges/${exchangeId}/cancel`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to cancel exchange request');
    }
  },

  async updateBookAvailability(bookId, available) {
    try {
      const response = await api.put(`/exchanges/book/${bookId}/availability`, { available });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to update book availability');
    }
  },

  // Helper methods for filtering exchanges
  async getSentExchanges(params = {}) {
    return this.getExchanges({ ...params, type: 'sent' });
  },

  async getReceivedExchanges(params = {}) {
    return this.getExchanges({ ...params, type: 'received' });
  },

  async getPendingExchanges(params = {}) {
    return this.getExchanges({ ...params, status: 'pending' });
  },

  async getApprovedExchanges(params = {}) {
    return this.getExchanges({ ...params, status: 'approved' });
  },

  async getCompletedExchanges(params = {}) {
    return this.getExchanges({ ...params, status: 'completed' });
  },

  // Exchange status actions
  async approveExchange(exchangeId, message = '') {
    return this.updateExchange(exchangeId, { status: 'approved', message });
  },

  async rejectExchange(exchangeId, message = '') {
    return this.updateExchange(exchangeId, { status: 'rejected', message });
  },

  async completeExchange(exchangeId, message = '') {
    return this.updateExchange(exchangeId, { status: 'completed', message });
  }
};

export default exchangeService;