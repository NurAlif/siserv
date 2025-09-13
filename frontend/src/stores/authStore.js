import { defineStore } from 'pinia';
import apiClient from '../services/api';
import router from '../router';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    error: null,
    isLoading: false,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token && !!state.user,
  },
  actions: {
    async signup(credentials) {
      this.isLoading = true;
      this.error = null;
      try {
        await apiClient.post('/auth/signup', credentials);
        // We don't log the user in automatically.
        // They will be redirected to log in after successful signup.
      } catch (err) {
        if (err.response && err.response.data && err.response.data.detail) {
             this.error = `Signup failed: ${err.response.data.detail}`;
        } else {
            this.error = 'An unknown error occurred during signup.';
        }
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },
    async login(credentials) {
      this.isLoading = true;
      this.error = null;
      try {
        // API expects form data for the token endpoint
        const formData = new URLSearchParams();
        formData.append('username', credentials.username);
        formData.append('password', credentials.password);

        const response = await apiClient.post('/auth/token', formData, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });

        const token = response.data.access_token;
        this.token = token;
        localStorage.setItem('token', token);

        // After getting token, fetch user profile
        await this.fetchUser();
        
        // Redirect to dashboard
        router.push('/');
      } catch (err) {
        this.error = 'Login failed. Please check your credentials.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },

    async fetchUser() {
        if (!this.token) return;
        try {
            const response = await apiClient.get('/auth/me');
            this.user = response.data;
        } catch (err) {
            console.error('Failed to fetch user:', err);
            // If fetching user fails (e.g., expired token), log them out
            this.logout();
        }
    },

    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem('token');
      router.push('/login');
    },
  },
});
