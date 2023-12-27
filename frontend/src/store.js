// src/store.js
// Importing necessary module to create Vuex store
import { createStore } from "vuex";

const store = createStore({
  // State of the Vuex store
  state: {
    // currentUser holds the data of the logged-in user, initially null
    currentUser: null,
    // authToken holds the authentication token, initially fetched from localStorage
    authToken: localStorage.getItem("userToken") || null,
  },
  // Mutations to change the state
  mutations: {
    // Set the currentUser in the state
    setCurrentUser(state, user) {
      state.currentUser = user;
    },
    // Set the authToken in the state and localStorage
    setAuthToken(state, token) {
      state.authToken = token;
      localStorage.setItem("userToken", token); // Save token to localStorage
    },
    // Clear the authToken from the state and localStorage
    clearAuthToken(state) {
      state.authToken = null;
      localStorage.removeItem("userToken"); // Remove token from localStorage
    },
  },
  // Actions to commit mutations
  actions: {
    // Update the currentUser in the state
    updateCurrentUser({ commit }, user) {
      commit("setCurrentUser", user);
    },
    // Update the authToken in the state
    updateAuthToken({ commit }, token) {
      commit("setAuthToken", token);
    },
    // Logout action to clear user and token from the state
    logout({ commit }) {
      commit("clearAuthToken");
      commit("setCurrentUser", null);
    },
  },
  // Getters to access state values
  getters: {
    // Get the current user from the state
    getCurrentUser: (state) => state.currentUser,
    // Check if a user is logged in
    isLoggedIn: (state) => !!state.currentUser,
    // Get the authentication token from the state
    getAuthToken: (state) => state.authToken, // Getter for the token
  },
});

export default store;
