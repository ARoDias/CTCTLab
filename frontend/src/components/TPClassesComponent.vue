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
    <!-- v-if="isQuestionnaireAnswered(currentQuestionnaireId)" -->
    <div
      class="graph-container"
      v-if="isQuestionnaireAnswered(currentQuestionnaireId)"
    >
      <h3>Obrigado pelas respostas!</h3>
      <ResultsGraph v-if="false" :question-details="questionDetails" />
    </div>

    <!-- Modal for displaying questions -->
    <QuestionsModal
      :show="showModal"
      @close="closeModal"
      :title="questionnaireTitle"
    >
      <!-- Modal header -->
      <template v-slot:header>
        <h3>{{ questionnaireTitle }}</h3>
      </template>

      <!-- Conditional rendering of questions or results -->
      <QuestionsComponent
        v-if="questionsAnswered < questions.length"
        :question="questions[questionsAnswered]"
        @question-answered="questionAnswered"
      />
      <!-- <ResultComponent v-else :result="results[totalCorrect]" /> -->
    </QuestionsModal>
  </div>
</template>

<script>
import apiClient from "@/axiosConfig";
import QuestionsModal from "@/components/QuestionsModal.vue";
import QuestionsComponent from "@/components/QuestionsComponent.vue";
// import ResultComponent from "@/components/ResultComponent.vue";
import ResultsGraph from "@/components/ResultsGraph.vue";
import { mapGetters } from "vuex";

export default {
  components: {
    QuestionsModal,
    QuestionsComponent,
    // ResultComponent,
    ResultsGraph,
  },
  data() {
    return {
      showModal: false,
      questionsAnswered: 0,
      totalCorrect: 0,
      questions: [],
      questionnaireTitle: "",
      results: [],
      currentActivity: 2,
      currentWeek: 3,
      questionnaires: [],
      currentQuestionnaireId: null,
      questionResponses: [],
      questionDetails: [],
    };
  },
  computed: {
    ...mapGetters(["isQuestionnaireAnswered"]),
    availableQuestionnaires() {
      // Only show questionnaires that have not been answered and are active
      return this.questionnaires.filter(
        (q) => !this.isQuestionnaireAnswered(q.id) && q.is_active
      );
    },
    questionIds() {
      return this.questions.map((question) => question.id);
    },
  },
  created() {
    this.initializeComponent();
    this.$store.dispatch("fetchAnsweredQuestionnaires").then(() => {
      this.fetchWeekQuestionnaires();
    });
  },
  methods: {
    initializeComponent() {
      //this.fetchActivityQuestionnaires();
      this.fetchWeekQuestionnaires();
    },
    fetchWeekQuestionnaires() {
      const url = `/api/questions/questionnaires/`;
      apiClient
        .get(url)
        .then((response) => {
          // Certifique-se de que a store Vuex foi carregada
          if (!this.$store.state.answeredQuestionnaires) {
            // Se não estiver definido, você pode querer carregar ou definir um valor padrão
            console.error("answeredQuestionnaires is not defined.");
            return;
          }

          const answeredIds = this.$store.state.answeredQuestionnaires;

          // Filtro que verifica a semana, se está ativo e se já foi respondido
          const availableQuestionnaires = response.data.filter(
            (q) =>
              q.week === this.currentWeek &&
              q.is_active &&
              !answeredIds.includes(q.id)
          );

          // Atualiza os questionários disponíveis
          this.questionnaires = availableQuestionnaires;
        })
        .catch((error) => {
          console.error("Error fetching questionnaires:", error);
        });
    },
    fetchActivityQuestionnaires() {
      // Fetch questionnaires for the current activity and week
      const url = `/api/questions/activities/${this.currentActivity}/questionnaires/?week_number=${this.currentWeek}`;
      apiClient
        .get(url)
        .then((response) => {
          this.questionnaires = response.data;
        })
        .catch((error) => {
          console.error("Error fetching questionnaires for activity:", error);
        });
    },
    fetchQuestions(questionnaireId) {
      // Reset questions and questionDetails before fetching new ones
      this.questions = [];
      this.questionDetails = [];
      this.currentQuestionnaireId = questionnaireId;
      this.questionsAnswered = 0; // Reset the count of answered questions

      // Fetch questions from the selected questionnaire
      apiClient
        .get(`/api/questions/questionnaires/${questionnaireId}/`)
        .then((response) => {
          // Assume that the response contains an array of question IDs
          const questionIds = response.data.questions;

          // Fetch details for each question
          return Promise.all(
            questionIds.map((qId) =>
              apiClient.get(`/api/questions/questions/${qId}/`)
            )
          );
        })
        .then((responses) => {
          // Set the fetched questions to the questions data property
          this.questions = responses.map((res) => res.data);

          // Prepare question details for the ResultsGraph component
          this.questionDetails = this.questions.map((q) => ({
            id: q.id,
            questionText: q.question_text,
            options: q.options.map((opt) => ({
              id: opt.id,
              optionText: opt.option_text,
              isCorrect: opt.is_correct,
            })),
          }));

          // Find the title for the current questionnaire
          const currentQuestionnaire = this.questionnaires.find(
            (q) => q.id === questionnaireId
          );
          this.questionnaireTitle = currentQuestionnaire
            ? currentQuestionnaire.title
            : "Questionnaire";

          // Show the modal with questions
          this.showModal = true;
        })
        .catch((error) => {
          console.error(
            `Error fetching questions for questionnaire ID ${questionnaireId}:`,
            error
          );
        });
    },
    closeModal() {
      this.showModal = false;
      this.reset();
    },
    questionAnswered(questionId, selectedOptionId) {
      // Record each question answered by the user
      this.questionResponses.push({
        question: questionId,
        selected_option: selectedOptionId,
      });
      this.questionsAnswered++;
      // Check if all questions have been answered
      if (this.questionsAnswered >= this.questions.length) {
        this.showModal = false;
        this.sendAllResponses();
      }
    },
    sendAllResponses() {
      // Send all responses to the server after answering all questions
      if (!this.currentQuestionnaireId) {
        console.error("Questionnaire ID not defined.");
        return;
      }
      const studentNumber = parseInt(this.$store.getters.getStudentNumber);
      if (!studentNumber) {
        alert("Student identification failed. Please log in again.");
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
        .then(() => {
          this.$store.dispatch(
            "markQuestionnaireAsAnswered",
            this.currentQuestionnaireId
          );
          this.reset();
        })
        .catch((error) => {
          console.error("Error sending question responses:", error);
        });
    },
    reset() {
      // Reset the state after closing the modal or sending responses
      this.questionsAnswered = 0;
      this.totalCorrect = 0;
      this.questionResponses = [];
      this.questionDetails = [];
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
