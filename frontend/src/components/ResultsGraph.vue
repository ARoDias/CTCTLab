<!-- components/ResultsGraph.vue -->
<template>
  <div>
    <!-- Buttons to switch between graphs -->
    <div class="graph-switch">
      <button @click="currentGraph = 'correctIncorrect'">
        Respostas Corretas
      </button>
      <button @click="currentGraph = 'distribution'">
        Distribuição das Respostas pelos Alunos
      </button>
    </div>
    <!-- Question Details -->
    <div class="question-details">
      <div
        v-for="(question, index) in questionDetails"
        :key="question.id"
        class="question-info"
      >
        <h3>Q{{ index + 1 }} - {{ question.questionText }}</h3>
        <p>Opção correta: {{ getCorrectOptionText(question) }}</p>
      </div>
    </div>

    <!-- Conditionally render the chart components -->
    <CorrectIncorrectChart
      v-show="currentGraph === 'correctIncorrect'"
      :doughnutChartData="doughnutChartData"
      :questionDetails="questionDetails"
    />

    <OptionDistributionChart
      v-show="currentGraph === 'distribution'"
      :optionDistributionData="optionDistributionData"
      :questionDetails="questionDetails"
    />
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
  props: {
    questionDetails: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      currentGraph: "correctIncorrect",
      doughnutChartData: [], // Data for CorrectIncorrectChart
      optionDistributionData: [], // Data for OptionDistributionChart
    };
  },
  async created() {
    await this.fetchData();
  },
  methods: {
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
