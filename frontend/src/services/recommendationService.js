import api from './api';

const recommendationService = {
  // Get personalized recommendations for the current user
  getRecommendations: async (limit = 10) => {
    try {
      const response = await api.get(`/recommendations?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      throw error;
    }
  },

  // Get books similar to a specific book
  getSimilarBooks: async (bookId, limit = 5) => {
    try {
      const response = await api.get(`/recommendations/similar/${bookId}?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching similar books:', error);
      throw error;
    }
  },

  // Record user interaction with a book
  recordInteraction: async (bookId, interactionType) => {
    try {
      const response = await api.post('/interactions', {
        book_id: bookId,
        interaction_type: interactionType
      });
      return response.data;
    } catch (error) {
      console.error('Error recording interaction:', error);
      // Don't throw error for interactions as they're background operations
      return null;
    }
  },

  // Get user's recommendation statistics
  getRecommendationStats: async () => {
    try {
      const response = await api.get('/recommendations/stats');
      return response.data;
    } catch (error) {
      console.error('Error fetching recommendation stats:', error);
      throw error;
    }
  },

  // Refresh recommendation model
  refreshRecommendations: async () => {
    try {
      const response = await api.post('/recommendations/refresh');
      return response.data;
    } catch (error) {
      console.error('Error refreshing recommendations:', error);
      throw error;
    }
  }
};

export default recommendationService;