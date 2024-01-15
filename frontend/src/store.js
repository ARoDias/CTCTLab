import { createStore } from "vuex";
import apiClient from "@/axiosConfig.js";

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
    authToken: getSavedState("authToken"),
    answeredQuestionnaires: getSavedState("answeredQuestionnaires") || [],
  },
  mutations: {
    setCurrentUser(state, userData) {
      state.currentUser = {
        ...userData,
        studentNumber: userData.is_student ? userData.username : null,
      };
      localStorage.setItem("currentUser", JSON.stringify(state.currentUser));
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
    setAnsweredQuestionnaires(state, questionnaires) {
      state.answeredQuestionnaires = questionnaires;
    },
    addAnsweredQuestionnaire(state, questionnaireId) {
      if (!state.answeredQuestionnaires.includes(questionnaireId)) {
        state.answeredQuestionnaires.push(questionnaireId);
        // Atualiza o localStorage
        console.log("A guardar questionários respondidos: ", questionnaireId);
        localStorage.setItem(
          "answeredQuestionnaires",
          JSON.stringify(state.answeredQuestionnaires)
        );
      }
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
    markQuestionnaireAsAnswered({ commit }, questionnaireId) {
      commit("addAnsweredQuestionnaire", questionnaireId);
    },
    async fetchAnsweredQuestionnaires({ commit, getters }) {
      if (getters.isLoggedIn) {
        try {
          const response = await apiClient.get(
            "/api/questions/studentresponses/"
          );
          const studentId = getters.getCurrentUser.id;
          const answeredQuestionnaires = response.data
            .filter((response) => response.student === studentId)
            .map((response) => response.questionnaire);

          commit("setAnsweredQuestionnaires", answeredQuestionnaires);
        } catch (error) {
          console.error("Error fetching answered questionnaires:", error);
        }
      }
    },
  },
  getters: {
    getCurrentUser: (state) => state.currentUser,
    isStudent: (state) => state.currentUser?.is_student,
    isTeacher: (state) => state.currentUser?.is_teacher,
    getStudentNumber: (state) => state.currentUser?.studentNumber,
    isLoggedIn: (state) => !!state.authToken,
    getAuthToken: (state) => state.authToken,
    isQuestionnaireAnswered: (state) => {
      console.log("Getting answered questionnaire", state);
      return (questionnaireId) => {
        return state.answeredQuestionnaires.includes(questionnaireId);
      };
    },
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
