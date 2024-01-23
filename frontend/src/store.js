import { createStore } from "vuex";
import apiClient from "@/axiosConfig.js";

function getSavedState(key) {
  //console.log(`Recuperando ${key} do localStorage...`);
  const value = localStorage.getItem(key);
  if (value === null || value === "undefined") {
    //console.log(`${key} não encontrado ou inválido no localStorage.`);
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
        studentProfileId: getSavedState("studentProfileId"),
        teacherProfileId: getSavedState("teacherProfileId"),
      };
      localStorage.setItem("currentUser", JSON.stringify(state.currentUser));
    },
    setStudentProfileId(state, profileId) {
      state.currentUser = { ...state.currentUser, studentProfileId: profileId };
      localStorage.setItem("studentProfileId", JSON.stringify(profileId));
    },
    setTeacherProfileId(state, profileId) {
      state.currentUser = { ...state.currentUser, teacherProfileId: profileId };
      localStorage.setItem("teacherProfileId", JSON.stringify(profileId));
    },
    setAuthToken(state, token) {
      state.authToken = token;
      localStorage.setItem("authToken", JSON.stringify(token));
    },
    clearAuthData(state) {
      state.currentUser = null;
      state.authToken = null;
      localStorage.removeItem("currentUser");
      localStorage.removeItem("authToken");
      localStorage.removeItem("studentProfileId");
      localStorage.removeItem("teacherProfileId");
    },
    setAnsweredQuestionnaires(state, questionnaires) {
      state.answeredQuestionnaires = questionnaires;
      localStorage.setItem(
        "answeredQuestionnaires",
        JSON.stringify(questionnaires)
      );
    },
    addAnsweredQuestionnaire(state, questionnaireId) {
      if (!state.answeredQuestionnaires.includes(questionnaireId)) {
        state.answeredQuestionnaires.push(questionnaireId);
        console.log("A guardar questionários respondidos: ", questionnaireId);
        localStorage.setItem(
          "answeredQuestionnaires",
          JSON.stringify(state.answeredQuestionnaires)
        );
      }
    },
  },
  actions: {
    async fetchAndSetUserProfile({ commit, state }) {
      if (state.currentUser.is_student) {
        try {
          const response = await apiClient.get("/api/users/students/");
          const userProfile = response.data.find(
            (profile) => profile.user.id === state.currentUser.id
          );
          if (userProfile) {
            commit("setStudentProfileId", userProfile.id);
          }
        } catch (error) {
          console.error("Error fetching student profile:", error);
        }
      } else if (state.currentUser.is_teacher) {
        try {
          const response = await apiClient.get("/api/users/teachers/");
          const userProfile = response.data.find(
            (profile) => profile.user.id === state.currentUser.id
          );
          if (userProfile) {
            commit("setTeacherProfileId", userProfile.id);
          }
        } catch (error) {
          console.error("Error fetching teacher profile:", error);
        }
      }
    },
    updateCurrentUser({ commit, dispatch }, userData) {
      commit("setCurrentUser", userData);
      dispatch("fetchAndSetUserProfile");
    },
    updateAuthToken({ commit }, token) {
      commit("setAuthToken", token);
    },
    logout({ commit }) {
      commit("clearAuthData");
    },
    markQuestionnaireAsAnswered({ commit }, questionnaireId) {
      commit("addAnsweredQuestionnaire", questionnaireId);
    },
    async fetchAnsweredQuestionnaires({ commit, state }) {
      if (state.authToken) {
        try {
          const response = await apiClient.get(
            "/api/questions/studentresponses/"
          );
          const studentId = state.currentUser.studentProfileId;
          const answeredQuestionnaires = response.data
            .filter((res) => res.student === studentId)
            .map((res) => res.questionnaire);
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
    getStudentProfileId: (state) => state.currentUser?.studentProfileId,
    getTeacherProfileId: (state) => state.currentUser?.teacherProfileId,
    isLoggedIn: (state) => !!state.authToken,
    getAuthToken: (state) => state.authToken,
    isQuestionnaireAnswered: (state) => (questionnaireId) =>
      state.answeredQuestionnaires.includes(questionnaireId),
  },
});

export default store;
