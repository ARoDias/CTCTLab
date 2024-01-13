import { createStore } from "vuex";

// Função para tentar recuperar um valor do localStorage e parsear de JSON
function getSavedState(key) {
  try {
    const value = localStorage.getItem(key);
    if (value && value !== "undefined") {
      return JSON.parse(value);
    }
  } catch (error) {
    console.error(`Erro ao recuperar ${key} do localStorage:`, error);
    localStorage.removeItem(key);
  }
  return null;
}

const store = createStore({
  state: {
    currentUser: getSavedState("currentUser"),
    userType: localStorage.getItem("userType") || null,
    studentNumber: localStorage.getItem("studentNumber") || null,
    authToken: localStorage.getItem("userToken") || null,
  },
  mutations: {
    setCurrentUser(state, userData) {
      state.currentUser = userData.user;
      state.userType = userData.userType;
      state.studentNumber =
        userData.userType === "student" ? userData.username : null;
      localStorage.setItem("currentUser", JSON.stringify(userData.user));
      localStorage.setItem("userType", userData.userType);
      if (userData.userType === "student") {
        localStorage.setItem("studentNumber", userData.username);
      } else {
        localStorage.removeItem("studentNumber");
      }
    },
    setAuthToken(state, token) {
      state.authToken = token;
      localStorage.setItem("userToken", token);
    },
    clearAuthData(state) {
      state.currentUser = null;
      state.userType = null;
      state.studentNumber = null;
      state.authToken = null;

      localStorage.removeItem("currentUser");
      localStorage.removeItem("userType");
      localStorage.removeItem("studentNumber");
      localStorage.removeItem("userToken");
    },
  },
  actions: {
    updateCurrentUser({ commit }, userData) {
      commit("setCurrentUser", userData);
    },
    updateAuthToken({ commit }, token) {
      commit("setAuthToken", token);
    },
    logout({ commit }) {
      commit("clearAuthData");
    },
  },
  getters: {
    getCurrentUser: (state) => state.currentUser,
    getUserType: (state) => state.userType,
    getStudentNumber: (state) => state.studentNumber,
    isLoggedIn: (state) => !!state.authToken,
    getAuthToken: (state) => state.authToken,
  },
});

export default store;
