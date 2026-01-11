import api from './api';

const authService = {
  async login(email, password) {
    try {
      const response = await api.post('/auth/login', {
        email,
        password,
      });

      const { tokens, user } = response.data;
      
      // Store tokens
      localStorage.setItem('token', tokens.access_token);
      localStorage.setItem('refreshToken', tokens.refresh_token);

      return { user, token: tokens.access_token };
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Login failed');
    }
  },

  async register(userData) {
    try {
      const response = await api.post('/auth/register', userData);

      const { tokens, user } = response.data;
      
      // Store tokens
      localStorage.setItem('token', tokens.access_token);
      localStorage.setItem('refreshToken', tokens.refresh_token);

      return { user, token: tokens.access_token };
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Registration failed');
    }
  },

  async getCurrentUser() {
    try {
      const response = await api.get('/auth/profile');
      return response.data.user;
    } catch (error) {
      throw new Error('Failed to get user profile');
    }
  },

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
  },

  getToken() {
    return localStorage.getItem('token');
  },

  isAuthenticated() {
    return !!this.getToken();
  },
};

export default authService;