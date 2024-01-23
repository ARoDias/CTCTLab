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
    <div
      class="graph-container"
      v-if="isQuestionnaireAnswered(currentQuestionnaireId)"
    >
      <ResultsGraph :question-details="questionDetails" />
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
// Importing components and utilities
import apiClient from "@/axiosConfig";
import QuestionsModal from "@/components/QuestionsModal.vue";
import QuestionsComponent from "@/components/QuestionsComponent.vue";
//import ResultComponent from "@/components/ResultComponent.vue";
import ResultsGraph from "@/components/ResultsGraph.vue";
import { mapGetters } from "vuex";

export default {
  components: {
    QuestionsModal,
    QuestionsComponent,
    //ResultComponent,
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
      currentActivity: 4,
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
      return this.questionnaires.filter(
        (q) => !this.isQuestionnaireAnswered(q.id)
      );
    },
    questionIds() {
      return this.questions.map((question) => question.id);
    },
  },
  created() {
    this.initializeComponent();
    this.$store.dispatch("fetchAnsweredQuestionnaires");
  },
  methods: {
    initializeComponent() {
      this.fetchActivityQuestionnaires();
    },
    fetchActivityQuestionnaires() {
      const url = `/api/questions/activities/${this.currentActivity}/questionnaires/?week_number=${this.currentWeek}`;
      apiClient
        .get(url)
        .then((response) => {
          this.questionnaires = response.data;
          //console.log(response.data);
        })
        .catch((error) => {
          console.error("Error fetching questionnaires for activity:", error);
        });
    },
    fetchQuestions(questionnaireId) {
      this.currentQuestionnaireId = questionnaireId;
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
          this.questionDetails = this.questions.map((q) => ({
            id: q.id,
            questionText: q.question_text,
            options: q.options.map((opt) => ({
              id: opt.id,
              optionText: opt.option_text,
              isCorrect: opt.is_correct,
            })),
          }));
          this.showModal = true;
          this.questionnaireTitle = this.questionnaires.find(
            (q) => q.id === questionnaireId
          ).title;
        })
        .catch((error) => {
          console.error("Error fetching questions", error);
        });
    },
    closeModal() {
      this.showModal = false;
      this.reset();
    },
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
        .then((responses) => {
          console.log("Responses successfully sent", responses);
          this.$store.dispatch(
            "markQuestionnaireAsAnswered",
            this.currentQuestionnaireId
          );
        })
        .catch((error) => {
          console.error("Error sending question responses:", error);
        });
      this.reset();
    },
    reset() {
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
