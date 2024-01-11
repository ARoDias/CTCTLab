// src/store.js
import { createStore } from "vuex";

const store = createStore({
  // State of the Vuex store
  state: {
    currentUser: null,
    userType: null, // New field to store the user type (student or teacher)
    studentNumber: null, // Store student number only for students
    authToken: localStorage.getItem("userToken") || null,
  },
  // Mutations to change the state
  mutations: {
    setCurrentUser(state, userData) {
      state.currentUser = userData.user;
      state.userType = userData.userType;
      state.studentNumber =
        userData.userType === "student" ? userData.username : null;
    },
    setAuthToken(state, token) {
      state.authToken = token;
      localStorage.setItem("userToken", token); // Save token to localStorage
    },
    clearAuthToken(state) {
      state.authToken = null;
      localStorage.removeItem("userToken"); // Remove token from localStorage
      state.currentUser = null;
      state.userType = null;
      state.studentNumber = null;
    },
  },
  // Actions to commit mutations
  actions: {
    updateCurrentUser({ commit }, userData) {
      commit("setCurrentUser", userData);
    },
    updateAuthToken({ commit }, token) {
      commit("setAuthToken", token);
    },
    logout({ commit }) {
      commit("clearAuthToken");
    },
  },
  // Getters to access state values
  getters: {
    getCurrentUser: (state) => state.currentUser,
    getUserType: (state) => state.userType, // Getter for user type
    getStudentNumber: (state) => state.studentNumber, // Getter for student number
    isLoggedIn: (state) => !!state.currentUser,
    getAuthToken: (state) => state.authToken,
  },
});

export default store;
