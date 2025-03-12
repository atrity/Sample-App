import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    loading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isLoading: (state) => state.loading,
    getError: (state) => state.error,
    getUser: (state) => state.user
  },

  actions: {
    async login(credentials) {
      try {
        this.loading = true
        this.error = null

        // Make API request to login
        const response = await axios.post('/api/auth/login', credentials)
        const { user, token } = response.data

        // Store token in localStorage
        localStorage.setItem('token', token)

        // Update state
        this.token = token
        this.user = user

        // Configure axios defaults
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`

        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Login failed'
        throw error
      } finally {
        this.loading = false
      }
    },

    async logout() {
      try {
        this.loading = true
        
        // Make API request to logout
        await axios.post('/api/auth/logout')

        // Clear local storage
        localStorage.removeItem('token')

        // Reset state
        this.token = null
        this.user = null
        this.error = null

        // Remove axios default header
        delete axios.defaults.headers.common['Authorization']
      } catch (error) {
        console.error('Logout failed:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchUser() {
      try {
        this.loading = true
        this.error = null

        // Make API request to get user data
        const response = await axios.get('/api/auth/user')
        this.user = response.data

        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch user data'
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateProfile(data) {
      try {
        this.loading = true
        this.error = null

        // Make API request to update profile
        const response = await axios.put('/api/auth/profile', data)
        this.user = response.data

        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to update profile'
        throw error
      } finally {
        this.loading = false
      }
    },

    async changePassword(data) {
      try {
        this.loading = true
        this.error = null

        // Make API request to change password
        await axios.put('/api/auth/password', data)
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to change password'
        throw error
      } finally {
        this.loading = false
      }
    },

    async forgotPassword(email) {
      try {
        this.loading = true
        this.error = null

        // Make API request for password reset
        await axios.post('/api/auth/forgot-password', { email })
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to send reset email'
        throw error
      } finally {
        this.loading = false
      }
    },

    async resetPassword(data) {
      try {
        this.loading = true
        this.error = null

        // Make API request to reset password
        await axios.post('/api/auth/reset-password', data)
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to reset password'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Initialize auth state
    async init() {
      if (this.token) {
        try {
          // Set axios default header
          axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
          
          // Fetch user data
          await this.fetchUser()
        } catch (error) {
          // Handle invalid token
          if (error.response?.status === 401) {
            this.logout()
          }
        }
      }
    }
  }
})
