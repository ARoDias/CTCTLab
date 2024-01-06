// src/store.js
import { createStore } from "vuex";

const store = createStore({
  // State of the Vuex store
  state: {
    currentUser: null,
    studentProfileId: null,
    authToken: localStorage.getItem("userToken") || null,
  },
  // Mutations to change the state
  mutations: {
    setCurrentUser(state, user) {
      state.currentUser = user;
    },
    setStudentProfileId(state, id) {
      state.studentProfileId = id;
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
    updateStudentProfileId({ commit }, id) {
      commit("setStudentProfileId", id);
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
    getCurrentUser: (state) => state.currentUser,
    getStudentProfileId: (state) => state.studentProfileId,
    isLoggedIn: (state) => !!state.currentUser,
    getAuthToken: (state) => state.authToken, // Getter for the token
  },
});

export default store;
