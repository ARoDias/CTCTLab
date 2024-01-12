import { createStore } from "vuex";

const store = createStore({
  state: {
    currentUser: null,
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
    clearAuthTokens(state) {
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
      commit("clearAuthTokens");
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

try {
  const currentUserData = localStorage.getItem("currentUser");
  if (currentUserData && currentUserData !== "undefined") {
    // Verifica se não é "undefined" como string
    store.state.currentUser = JSON.parse(currentUserData);
  }
} catch (error) {
  console.error(
    "Erro ao analisar dados de currentUser do localStorage:",
    error
  );
  // Limpar o localStorage ou tomar outra ação apropriada
  localStorage.removeItem("currentUser");
  store.dispatch("logout");
}
export default store;
