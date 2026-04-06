import { create } from 'zustand';
import api from '../api/axios';

const useAuthStore = create((set, get) => ({
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: !!localStorage.getItem('token'),
  loading: false,
  error: null,

  login: async (username, password) => {
    set({ loading: true, error: null });
    try {
      console.log('Sending login request:', { username, password });
      const response = await api.post('auth/login/', { username, password });
      console.log('Login response:', response.data);
      const { access } = response.data;

      localStorage.setItem('token', access);
      console.log('Token saved to localStorage:', access);

      // Fetch full user data from /api/users/me/
      const userResponse = await api.get('users/me/', {
        headers: { 'Authorization': `Bearer ${access}` }
      });
      console.log('User data:', userResponse.data);

      set({
        token: access,
        user: userResponse.data,
        isAuthenticated: true,
        loading: false
      });

      return { success: true };
    } catch (error) {
      console.error('Login error:', error.response?.data || error);
      const errorMessage = error.response?.data?.message || 'Login failed';
      set({
        error: errorMessage,
        loading: false
      });
      return { success: false, error: errorMessage };
    }
  },

  register: async (name, email, password) => {
    set({ loading: true, error: null });
    try {
      const response = await api.post('auth/register/', { name, email, password });
      const { access } = response.data;

      localStorage.setItem('token', access);
      console.log('Token saved to localStorage:', access);

      // Fetch full user data from /api/users/me/ with auth header
      const userResponse = await api.get('users/me/', {
        headers: { 'Authorization': `Bearer ${access}` }
      });

      set({
        token: access,
        user: userResponse.data,
        isAuthenticated: true,
        loading: false
      });

      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Registration failed';
      set({
        error: errorMessage,
        loading: false
      });
      return { success: false, error: errorMessage };
    }
  },

  logout: () => {
    localStorage.removeItem('token');
    delete api.defaults.headers.common['Authorization'];
    set({
      token: null,
      user: null,
      isAuthenticated: false,
      error: null
    });
  },

  fetchCurrentUser: async () => {
    const token = localStorage.getItem('token');
    console.log('Fetching current user, token from localStorage:', token);
    if (!token) return;

    try {
      const response = await api.get('users/me/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      set({ user: response.data });
    } catch (error) {
      console.error('Failed to fetch user:', error.response?.data || error);
    }
  },

  clearError: () => set({ error: null }),
}));

export default useAuthStore;
