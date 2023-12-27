<template>
  <div>
    <!-- Loop through questionnaires and create a button for each one -->
    <button
      v-for="questionnaire in questionnaires"
      :key="questionnaire.id"
      @click="fetchQuestions(questionnaire.id)"
    >
      {{ questionnaire.title }}
    </button>

    <!-- Modal for displaying questions -->
    <QuestionsModal
      :show="showModal"
      @close="closeModal"
      :title="questionnaireTitle"
    >
      <!-- Slot for modal header -->
      <template v-slot:header>
        <h3>{{ questionnaireTitle }}</h3>
      </template>

      <!-- Conditional rendering of questions or results -->
      <QuestionsComponent
        v-if="questionsAnswered < questions.length"
        :question="questions[questionsAnswered]"
        @question-answered="questionAnswered"
      />
      <ResultComponent v-else :result="results[totalCorrect]" />
    </QuestionsModal>
  </div>
</template>

<script>
// Import the apiClient instance from axiosConfig
import apiClient from "@/axiosConfig";
import QuestionsModal from "@/components/QuestionsModal.vue";
import QuestionsComponent from "@/components/QuestionsComponent.vue";
import ResultComponent from "@/components/ResultComponent.vue";

export default {
  components: {
    QuestionsModal,
    QuestionsComponent,
    ResultComponent,
  },
  data() {
    return {
      showModal: false,
      questionsAnswered: 0,
      totalCorrect: 0,
      questions: [],
      questionnaireTitle: "",
      results: [], // Configuration for results
      currentActivity: 2, // Example activity ID
      currentWeek: 3, // Example week number
      questionnaires: [], // To store questionnaires for the current activity
      currentQuestionnaireId: null, // To keep track of the current questionnaire ID
      questionResponses: [], // To store user responses
    };
  },
  created() {
    this.fetchActivityQuestionnaires();
  },
  methods: {
    fetchActivityQuestionnaires() {
      const url = `/api/questions/activities/2/questionnaires/?week_number=3`;
      console.log("Requesting GET to:", url); // Logging for debugging
      apiClient
        .get(url)
        .then((response) => {
          console.log("Response received:", response.data);
          this.questionnaires = response.data;
        })
        .catch((error) => {
          console.error("Error fetching questionnaires for activity:", error);
        });
    },

    fetchQuestions(questionnaireId) {
      this.currentQuestionnaireId = questionnaireId;
      // Retrieve the question IDs for the selected questionnaire
      apiClient
        .get(`/api/questions/questionnaires/${questionnaireId}/`)
        .then((response) => {
          const questionIds = response.data.questions;
          return Promise.all(
            questionIds.map((qId) =>
              apiClient.get(`/api/questions/questions/${qId}/`)
            )
          );
        })
        .then((responses) => {
          this.questions = responses.map((res) => res.data);
          this.showModal = true;
          this.questionnaireTitle = this.questionnaires.find(
            (q) => q.id === questionnaireId
          ).title;
        })
        .catch((error) => {
          console.error("Error fetching questions", error);
          alert("Erro ao carregar as perguntas. Tente novamente.");
        });
    },

    closeModal() {
      this.showModal = false;
      this.reset();
    },
    sendResponse(questionId, selectedOptionId) {
      // Verifica se o ID do questionário está definido
      if (!this.currentQuestionnaireId) {
        alert("Erro ao identificar o questionário. Tenta novamente.");
        return;
      }

      // Obtém o ID do estudante autenticado
      const studentId = this.$store.getters.getCurrentUser?.id;
      if (!studentId) {
        alert(
          "Não foi possível identificar o utilizador. Por favor, faça login novamente."
        );
        return;
      }

      // Cria a StudentQuestionnaireResponse
      const studentQuestionnaireResponse = {
        student: studentId,
        questionnaire: this.currentQuestionnaireId,
      };

      // Envia a StudentQuestionnaireResponse
      apiClient
        .post("/api/questions/studentresponses/", studentQuestionnaireResponse)
        .then((response) => {
          const studentResponseId = response.data.id;
          // Agora com o ID da resposta do questionário, envia a resposta da pergunta
          const questionResponseDetail = {
            student_response: studentResponseId,
            question: questionId,
            selected_option: selectedOptionId,
          };
          return apiClient.post(
            "/api/questions/questionresponsedetails/",
            questionResponseDetail
          );
        })
        .then((response) => {
          console.log("Resposta enviada com sucesso:", response.data);
        })
        .catch((error) => {
          console.error("Erro ao enviar resposta da questão:", error);
          alert(
            "Ocorreu um erro ao enviar a resposta. Por favor, tente novamente."
          );
        });
    },

    questionAnswered(questionId, selectedOptionId, isCorrect) {
      // Adiciona a resposta atual ao array de respostas
      this.questionResponses.push({ questionId, selectedOptionId, isCorrect });
      // Incrementa o contador de perguntas respondidas
      this.questionsAnswered++;
      // Verifica se todas as perguntas foram respondidas
      if (this.questionsAnswered >= this.questions.length) {
        this.showModal = false;
        this.sendAllResponses();
      }
    },

    sendAllResponses() {
      if (!this.currentQuestionnaireId) {
        console.error("Questionnaire ID not defined.");
        alert("Erro ao identificar o questionário. Tenta novamente.");
        return;
      }

      const studentId = this.$store.getters.getCurrentUser?.id;
      if (!studentId) {
        alert(
          "Não foi possível identificar o utilizador. Por favor, faça login novamente."
        );
        return;
      }

      // Cria a StudentQuestionnaireResponse
      const studentQuestionnaireResponse = {
        student: studentId,
        questionnaire: this.currentQuestionnaireId,
      };

      let url = `/api/questions/studentresponses/`;
      apiClient
        .post(url, studentQuestionnaireResponse)
        .then((response) => {
          const studentResponseId = response.data.id;
          return Promise.all(
            this.questionResponses.map(({ questionId, selectedOptionId }) => {
              const questionResponseDetail = {
                student_response: studentResponseId,
                question: questionId,
                selected_option: selectedOptionId,
              };
              return apiClient.post(
                `/api/questions/questionresponsedetails/`,
                questionResponseDetail
              );
            })
          );
        })
        .then((responses) => {
          console.log(
            "Todas as respostas foram enviadas com sucesso",
            responses
          );
        })
        .catch((error) => {
          console.error("Erro ao enviar respostas das questões:", error);
          alert(
            "Ocorreu um erro ao enviar as respostas. Por favor, tente novamente."
          );
        });
    },

    reset() {
      // Reset the questionnaire state
      this.questionsAnswered = 0;
      this.totalCorrect = 0;
    },
  },
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}
body {
  font-size: 20px;
  font-family: sans-serif;
  padding-top: 20px;
  background: #e6ecf1;
}
</style>
