// src/store.js
import { createStore } from 'vuex'

const store = createStore({
  // State: Holds data that is shared across the application.
  state: {
    currentUser: null
  },
  
  // Mutations: Responsible for directly modifying the state.
  mutations: {
    // Set the current user in the state.
    setCurrentUser(state, user) {
      state.currentUser = user;
    }
  },

  // Actions: Used to commit mutations and can contain asynchronous operations.
  actions: {
    // Action to update the current user in the state.
    updateCurrentUser({ commit }, user) {
      commit('setCurrentUser', user);
    },

    // Action to handle user logout.
    logout({ commit }) {
      // Remove user token from localStorage.
      localStorage.removeItem('userToken');
      // Clear the current user from the state.
      commit('setCurrentUser', null);
    }
  },

  // Getters: Used to access and return computed state values.
  getters: {
    // Retrieve the current user from the state.
    getCurrentUser: state => state.currentUser,
    // Check if a user is authenticated.
    isLoggedIn: state => !!state.currentUser
  }
});

export default store;
