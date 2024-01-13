import { createStore } from "vuex";

function getSavedState(key) {
  console.log(`Recuperando ${key} do localStorage...`);
  const value = localStorage.getItem(key);
  if (value === null || value === "undefined") {
    console.log(`${key} não encontrado ou inválido no localStorage.`);
    return null;
  }
  try {
    return JSON.parse(value);
  } catch (error) {
    //console.error(`Erro ao recuperar ${key} do localStorage:`, error);
    localStorage.removeItem(key);
    return null;
  }
}

const store = createStore({
  state: {
    currentUser: getSavedState("currentUser"),
    studentNumber: getSavedState("studentNumber"),
    authToken: getSavedState("authToken"),
  },
  mutations: {
    setCurrentUser(state, userData) {
      //console.log("Mutation: Atualizando currentUser:", userData);
      state.currentUser = userData;
      state.studentNumber = userData.is_student ? userData.username : null;
      localStorage.setItem("currentUser", JSON.stringify(userData));
      if (userData.is_student) {
        localStorage.setItem(
          "studentNumber",
          JSON.stringify(userData.username)
        );
      } else {
        localStorage.removeItem("studentNumber");
      }
    },
    setAuthToken(state, token) {
      //console.log("Mutation: Atualizando authToken:", token);
      state.authToken = token;
      localStorage.setItem("authToken", JSON.stringify(token));
    },
    clearAuthData(state) {
      //console.log("Mutation: Limpando dados de autenticação...");
      state.currentUser = null;
      state.studentNumber = null;
      state.authToken = null;

      localStorage.removeItem("currentUser");
      localStorage.removeItem("studentNumber");
      localStorage.removeItem("authToken");
    },
  },
  actions: {
    updateCurrentUser({ commit }, userData) {
      //console.log("Action: updateCurrentUser chamada com:", userData);
      commit("setCurrentUser", userData);
    },
    updateAuthToken({ commit }, token) {
      //console.log("Action: updateAuthToken chamada com:", token);
      commit("setAuthToken", token);
    },
    logout({ commit }) {
      //console.log("Action: logout chamada.");
      commit("clearAuthData");
    },
  },
  getters: {
    getCurrentUser: (state) => state.currentUser,
    isStudent: (state) => state.currentUser?.is_student,
    isTeacher: (state) => state.currentUser?.is_teacher,
    getStudentNumber: (state) => state.studentNumber,
    isLoggedIn: (state) => !!state.authToken,
    getAuthToken: (state) => state.authToken,
  },
});

// Loading the authToken when the store is created
const authToken = getSavedState("authToken");
if (authToken) {
  //console.log("authToken encontrado durante a inicialização da store:", authToken);
  store.commit("setAuthToken", authToken);
} else {
  console.log("Nenhum authToken encontrado durante a inicialização da store.");
}

export default store;
