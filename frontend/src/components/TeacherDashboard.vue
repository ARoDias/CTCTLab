<!-- components/TeacherDashboard.vue -->
<template>
  <div>
    <!-- Buttons to switch between graphs -->
    <div class="graph-switch">
      <button @click="showCorrectIncorrectChart">Respostas Corretas</button>
      <button @click="showOptionDistributionChart">
        Distribuição das Respostas pelos Alunos
      </button>
    </div>
    <div class="graph-container">
      <!-- CorrectIncorrectChart Component with question details -->
      <div v-if="currentGraph === 'correctIncorrect'">
        <CorrectIncorrectChart
          :doughnutChartData="doughnutChartData"
          :shouldRenderChart="currentGraph === 'correctIncorrect'"
        >
          <!-- Slotted content for question details -->
          <div class="question-details" v-if="questionDetails.length">
            <div
              v-for="(question, index) in questionDetails"
              :key="question.id"
              class="question-info"
            >
              <h3>Q{{ index + 1 }} - {{ question.questionText }}</h3>
              <p>Opção correta: {{ getCorrectOptionText(question) }}</p>
            </div>
          </div>
        </CorrectIncorrectChart>
      </div>

      <!-- OptionDistributionChart Component with question details and options -->
      <div v-if="currentGraph === 'distribution'">
        <OptionDistributionChart
          :optionDistributionData="optionDistributionData"
        >
          <!-- Slotted content for question details with colors -->
          <template v-slot:default>
            <div
              class="question-details"
              v-if="questionDetails.length && optionDistributionData.length"
            >
              <div
                v-for="(question, qIndex) in questionDetails"
                :key="question.id"
                class="question-info"
              >
                <h3 :style="getStyle(qIndex)">
                  Q{{ qIndex + 1 }} - {{ question.questionText }}
                </h3>
                <ul>
                  <li
                    v-for="(option, oIndex) in question.options"
                    :key="oIndex"
                  >
                    <span
                      :style="{
                        fontWeight: 'bold',
                        color: getStyle(qIndex).color,
                      }"
                      >Opção {{ oIndex + 1 }} -</span
                    >
                    {{ option.optionText }}
                  </li>
                </ul>
              </div>
            </div>
          </template>
        </OptionDistributionChart>
      </div>
    </div>
  </div>
</template>

<script>
import CorrectIncorrectChart from "./CorrectIncorrectChart.vue";
import OptionDistributionChart from "./OptionDistributionChart.vue";
import apiClient from "@/axiosConfig";

export default {
  components: {
    CorrectIncorrectChart,
    OptionDistributionChart,
  },
  data() {
    return {
      currentGraph: null,
      doughnutChartData: [],
      optionDistributionData: [],
      questionDetails: [], // This will now be set internally
    };
  },
  async mounted() {
    await this.fetchLastAnsweredQuestionnaire();
    await this.fetchData();
  },
  methods: {
    async fetchLastAnsweredQuestionnaire() {
      try {
        //console.log("Fetching last answered questionnaire...");
        const response = await apiClient.get(
          "/api/questions/last_answered_questionnaire/"
        );
        //console.log("Last answered questionnaire data:", response.data);
        const lastAnsweredQuestionnaire = response.data;
        if (lastAnsweredQuestionnaire) {
          await this.fetchQuestions(lastAnsweredQuestionnaire.questionnaire);
        } else {
          console.log("No last answered questionnaire found");
        }
      } catch (error) {
        console.error("Error fetching the last answered questionnaire:", error);
      }
    },

    async fetchQuestions(questionnaireId) {
      try {
        //console.log(`Fetching questions for questionnaire ID: ${questionnaireId}`);
        const response = await apiClient.get(
          `/api/questions/questionnaires/${questionnaireId}/`
        );
        //console.log("Questions response:", response.data);
        const questionIds = response.data.questions;

        const questionsResponses = await Promise.all(
          questionIds.map((qId) =>
            apiClient.get(`/api/questions/questions/${qId}/`)
          )
        );

        this.questionDetails = questionsResponses.map((res) => {
          const q = res.data;
          return {
            id: q.id,
            questionText: q.question_text,
            options: q.options.map((opt) => ({
              id: opt.id,
              optionText: opt.option_text,
              isCorrect: opt.is_correct,
            })),
          };
        });

        // Now that questionDetails is set, fetch data for the charts
        await this.fetchData();
      } catch (error) {
        console.error("Error fetching questions for questionnaire", error);
      }
    },
    async showCorrectIncorrectChart() {
      this.currentGraph = "correctIncorrect";
      await this.fetchDataForCorrectIncorrectChart();
    },

    async showOptionDistributionChart() {
      this.currentGraph = "distribution";
      await this.fetchDataForOptionDistributionChart();
    },

    async fetchDataForCorrectIncorrectChart() {
      // Fetch only the data required for the CorrectIncorrectChart
      await this.fetchQuestionStats();
    },

    async fetchDataForOptionDistributionChart() {
      // Fetch only the data required for the OptionDistributionChart
      await this.fetchOptionDistribution();
    },
    getStyle(qIndex) {
      if (
        this.optionDistributionData &&
        this.optionDistributionData.length > qIndex
      ) {
        return {
          color:
            this.optionDistributionData[qIndex].backgroundColor + " !important",
          "font-weight": "bold",
        };
      }
      return {}; // Default style if data is not available
    },
    getCorrectOptionText(question) {
      const correctOption = question.options.find((option) => option.isCorrect);
      return correctOption ? correctOption.optionText : "Unknown";
    },
    // Fetch data for the charts
    async fetchData() {
      await this.fetchQuestionStats();
      await this.fetchOptionDistribution();
    },
    // Fetch statistics for correct/incorrect answers
    async fetchQuestionStats() {
      try {
        if (!this.questionDetails.length) {
          throw new Error("No question details provided");
        }
        const questionIds = this.questionDetails.map((q) => q.id);
        const response = await apiClient.get("/api/questions/stats/", {
          params: { question_ids: questionIds.join(",") },
        });
        this.doughnutChartData = response.data.map((q) => ({
          title: `Questão ${q.question_id}`,
          correct: q.correct_count,
          incorrect: q.incorrect_count,
        }));
      } catch (error) {
        console.error("Error fetching question stats:", error);
      }
    },
    // Fetch distribution data for the options
    async fetchOptionDistribution() {
      try {
        if (!this.questionDetails.length) {
          throw new Error("No question details provided");
        }
        const questionIds = this.questionDetails.map((q) => q.id);
        const response = await apiClient.get("/api/questions/opt_dist/", {
          params: { question_ids: questionIds.join(",") },
        });
        this.optionDistributionData = response.data.map((data) => {
          return {
            question_id: data.question_id,
            distribution: data.distribution.map((opt) => opt.count),
            backgroundColor: this.getRandomColor(), // Generate random color for each series
          };
        });
      } catch (error) {
        console.error("Error fetching option distribution data:", error);
      }
    },
    // Generate a random color
    getRandomColor() {
      return `#${Math.floor(Math.random() * 16777215).toString(16)}`;
    },
  },
};
</script>

<style>
.graph-switch button {
  margin: 10px;
  padding: 5px 15px;
  border: 1px solid var(--dark-blue);
  background-color: var(--vt-c-indigo);
  color: var(--white);
  cursor: pointer;
}
.graph-switch button:focus {
  outline: none;
  border-color: var(--primary-blue);
}
.question-details {
  padding: 1rem;
  background-color: var(--white);
  border-radius: var(--border-radius);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  margin-top: 1rem; /* Adds space between the charts and text */
}

.question-info {
  margin-bottom: 1.5rem; /* Space between each question info */
}

.question-info h3 {
  font-size: 1rem; /* Adjust font size for heading */
  color: var(--dark-blue); /* Color for the question text */
  margin: 0.5rem 0; /* Margin around the question */
}

.question-info p {
  font-size: 0.9rem; /* Adjust font size for paragraph */
  color: var(--vt-c-black); /* Color for the correct option text */
  margin: 0.5rem 0; /* Margin around the option text */
}

@media (max-width: 768px) {
  .question-info h3 {
    font-size: 0.9rem; /* Smaller font size for mobile */
  }

  .question-info p {
    font-size: 0.8rem; /* Smaller font size for mobile */
  }
}

/* Styles for Chart.js canvas containers to prevent overflow and improve responsiveness */
.chart-container,
.bar-chart-container,
.doughnut-chart-container {
  width: 100%;
  overflow: hidden; /* Prevents horizontal scroll on small devices */
  margin: 0 auto; /* Centers the chart */
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
}

.bar-chart-container {
  /* Specific styles for the bar chart container */
  flex: 1 0 100%; /* Take full width on larger screens */
  max-width: 90%; /* Limit the maximum width to avoid being too wide */
  margin-bottom: 20px; /* Space below the bar chart */
}

/* Ensure the canvas does not exceed the width of the container */
canvas {
  max-width: 100% !important; /* Overrides any inline styles set by Chart.js */
}

/* Styles specifically for doughnut charts */
.doughnut-chart-container {
  /* Specific styles for doughnut chart containers */
  flex: 1 0 45%; /* Take up to 45% of the container width */
}

.doughnut-chart-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  align-items: center;
}

@media (max-width: 480px) {
  .doughnut-chart-container {
    width: 100%; /* Each doughnut chart takes full width on smaller screens */
    margin-bottom: 1rem; /* Adds space between the doughnut charts */
  }

  .doughnut-chart-row {
    flex-direction: column; /* Stack doughnut charts vertically on small screens */
  }
}

/* Additional responsive adjustments for better mobile viewing */
@media (max-width: 480px) {
  .bar-chart-container {
    padding: 0 1rem; /* Adds padding to the sides for smaller screens */
  }

  .question-details {
    padding: 0.5rem; /* Reduces padding for text content on smaller screens */
  }
}
</style>
