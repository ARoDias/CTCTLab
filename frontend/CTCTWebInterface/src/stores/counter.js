// src/stores/counter.js
import { defineStore } from 'pinia'

// Define a new store using the `defineStore` function
export const useUserStore = defineStore('user', {
  // State: Holds data that is shared across the application.
  state: () => ({
    currentUser: null
  }),

  // Actions: Functions that can modify the state and can contain asynchronous operations.
  actions: {
    // Action to update the current user in the state.
    updateCurrentUser(user) {
      this.currentUser = user
    },

    // Action to handle user logout.
    logout() {
      // Remove user token from localStorage.
      localStorage.removeItem('userToken')
      // Clear the current user from the state.
      this.currentUser = null
    }
  },

  // Getters: Computed values based on the state.
  getters: {
    // Retrieve the current user from the state.
    getCurrentUser: (state) => state.currentUser,
    // Check if a user is authenticated.
    isLoggedIn: (state) => !!state.currentUser
  }
})
