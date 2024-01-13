<!-- components/TPClassesComponent.vue -->
<template>
  <div>
    <!-- Questionnaire buttons -->
    <div class="questionnaire-buttons">
      <button
        v-for="questionnaire in availableQuestionnaires"
        :key="questionnaire.id"
        @click="fetchQuestions(questionnaire.id)"
      >
        {{ questionnaire.title }}
      </button>
    </div>

    <!-- Graph Container -->
    <div class="graph-container">
      <ResultsGraph :question-ids="questionIds" />
    </div>

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
import ResultsGraph from "@/components/ResultsGraph.vue";

export default {
  components: {
    QuestionsModal,
    QuestionsComponent,
    ResultComponent,
    ResultsGraph,
  },
  data() {
    return {
      showModal: false,
      questionsAnswered: 0,
      totalCorrect: 0,
      questions: [],
      questionnaireTitle: "",
      results: [], // Configuration for results
      currentActivity: 1, // Example activity ID
      currentWeek: 3, // Example week number
      questionnaires: [], // To store questionnaires for the current activity
      currentQuestionnaireId: null, // To keep track of the current questionnaire ID
      questionResponses: [], // To store user responses
      answeredQuestionnaires: new Set(),
    };
  },
  computed: {
    availableQuestionnaires() {
      return this.questionnaires.filter(
        (q) => !this.answeredQuestionnaires.has(q.id)
      );
    },
    questionIds() {
      return this.questions.map((question) => question.id);
    },
  },
  created() {
    this.fetchActivityQuestionnaires();
  },
  methods: {
    fetchActivityQuestionnaires() {
      const url = `/api/questions/activities/${this.currentActivity}/questionnaires/?week_number=${this.currentWeek}`;
      //console.log("Requesting GET to:", url); // Logging for debugging
      apiClient
        .get(url)
        .then((response) => {
          //console.log("Response received:", response.data);
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
    // Send individual question response
    sendResponse(questionId, selectedOptionId) {
      const responseDetail = {
        question: questionId,
        selected_option: selectedOptionId,
      };
      this.questionResponses.push(responseDetail);
    },

    // Handle when a question is answered
    questionAnswered(questionId, selectedOptionId) {
      this.questionResponses.push({
        question: questionId,
        selected_option: selectedOptionId,
      });

      this.questionsAnswered++;

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

      const studentNumber = parseInt(this.$store.getters.getStudentNumber);

      if (!studentNumber) {
        alert(
          "Não foi possível identificar o estudante. Por favor, faça login novamente."
        );
        return;
      }

      const studentQuestionnaireResponse = {
        student_number: studentNumber,
        questionnaire: this.currentQuestionnaireId,
        response_details: this.questionResponses,
      };

      let url = "/api/questions/create_student_responses/";
      apiClient
        .post(url, studentQuestionnaireResponse)
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
      // Mark the questionnaire as answered
      this.answeredQuestionnaires.add(this.currentQuestionnaireId);
      this.reset();
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
  background: var(--light-blue);
}

.questionnaire-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center; /* Center buttons */
}

.questionnaire-buttons button {
  padding: 10px 15px;
  border: none;
  background-color: var(--primary-blue); /* Use variable */
  color: var(--white);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.questionnaire-buttons button:hover {
  background-color: var(--dark-blue); /* Use variable */
}

@media (max-width: 768px) {
  .questionnaire-buttons {
    flex-direction: column;
  }
}
</style>
