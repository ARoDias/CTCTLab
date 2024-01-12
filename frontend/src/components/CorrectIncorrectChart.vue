<!-- components/CorrectIncorrectChart.vue -->
<template>
  <div>
    <!-- Bar Chart -->
    <div class="bar-chart-container">
      <canvas ref="barChart"></canvas>
    </div>
    <!-- Doughnut Chart Rows -->
    <div class="doughnut-chart-row">
      <div
        v-for="(data, index) in doughnutChartData"
        :key="index"
        class="doughnut-chart-container"
      >
        <!-- Add title above each doughnut chart -->
        <canvas :ref="'doughnutChart' + index"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
import apiClient from "@/axiosConfig";
Chart.register(...registerables);

export default {
  props: {
    questionIds: Array, // Receive question IDs as a prop from the parent component
  },
  data() {
    return {
      barChart: null,
      doughnutCharts: [],
      doughnutChartData: [], // Initially empty, will be filled with real data
    };
  },
  async mounted() {
    await this.fetchQuestionStats();
    this.createDoughnutCharts();
    this.createBarChart();
  },
  beforeUnmount() {
    if (this.barChart) {
      this.barChart.destroy();
    }
    this.doughnutCharts.forEach((chart) => chart && chart.destroy());
  },
  methods: {
    async fetchQuestionStats() {
      try {
        if (this.questionIds.length === 0) {
          throw new Error("No question IDs provided");
        }
        const response = await apiClient.get("/api/questions/stats/", {
          params: { question_ids: this.questionIds.join(",") }, // Ensure this is sent correctly
        });
        this.doughnutChartData = response.data.map((q) => ({
          title: `Question ${q.question_id}`,
          correct: q.correct_count,
          incorrect: q.incorrect_count,
        }));
        this.updateCharts(); // Call a method to update the charts with new data
      } catch (error) {
        console.error("Error fetching question stats:", error);
      }
    },
    createBarChart() {
      const barData = {
        labels: ["Q1", "Q2", "Q3", "Q4", "Q5"],
        datasets: [
          {
            label: "Correct Answers",
            backgroundColor: "green",
            data: this.doughnutChartData.map((d) => d.correct),
          },
          {
            label: "Incorrect Answers",
            backgroundColor: "red",
            data: this.doughnutChartData.map((d) => d.incorrect),
          },
        ],
      };
      const barOptions = {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
        responsive: true,
        maintainAspectRatio: false,
      };
      this.barChart = new Chart(this.$refs.barChart.getContext("2d"), {
        type: "bar",
        data: barData,
        options: barOptions,
      });
    },
    createDoughnutCharts() {
      // Clear existing charts before creating new ones
      this.doughnutCharts.forEach((chart) => chart && chart.destroy());
      this.doughnutCharts = [];
      this.doughnutChartData.forEach((data, index) => {
        this.$nextTick(() => {
          // Ensure that the canvas element is the first item in the array for this ref.
          const canvas = this.$refs["doughnutChart" + index][0];
          if (!canvas) {
            // If the canvas is not found, log an error or handle appropriately
            console.error(`Canvas for doughnutChart${index} not found`);
            return;
          }
          const context = canvas.getContext("2d");
          const chart = new Chart(context, {
            type: "doughnut",
            data: {
              labels: ["Correct", "Incorrect"],
              datasets: [
                {
                  data: [data.correct, data.incorrect],
                  backgroundColor: ["green", "red"],
                },
              ],
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              legend: {
                display: false,
              },
              plugins: {
                legend: {
                  display: false,
                },
                title: {
                  display: true,
                  text: data.title, // Set the title for each doughnut chart
                },
              },
            },
          });
          this.doughnutCharts.push(chart);
        });
      });
    },
    updateCharts() {
      // Method to update both bar and doughnut charts
      this.createBarChart();
      this.createDoughnutCharts();
    },
  },
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

body,
html {
  max-width: 100vw;
  overflow-x: hidden;
}

.chart-container,
.doughnut-chart-container {
  /* Shared styles for chart containers */
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  margin: 0 auto; /* Center the charts and prevent horizontal overflow */
  max-width: 100%; /* Ensure the container does not exceed the width of the viewport */
}

.bar-chart-container {
  /* Specific styles for the bar chart container */
  flex: 1 0 100%; /* Take full width on larger screens */
  max-width: 90%; /* Limit the maximum width to avoid being too wide */
  margin-bottom: 20px; /* Space below the bar chart */
}

.doughnut-chart-container {
  /* Specific styles for doughnut chart containers */
  flex: 1 0 45%; /* Take up to 45% of the container width */
}

.doughnut-chart-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

@media (max-width: 768px) {
  .doughnut-chart-container {
    flex-basis: 100%; /* Each doughnut chart takes full width on medium screens */
  }
}

@media (max-width: 480px) {
  .doughnut-chart-container {
    flex-basis: 100%; /* Each doughnut chart takes full width on small screens */
  }
}
</style>
