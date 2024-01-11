<template>
  <div>
    <!-- Bar Chart -->
    <div class="chart-container">
      <canvas ref="barChart"></canvas>
    </div>
    <!-- Doughnut Chart Rows -->
    <div class="doughnut-chart-row">
      <div class="chart-container" v-for="index in [0, 1]" :key="index">
        <canvas :ref="'doughnutChart' + index"></canvas>
      </div>
    </div>
    <div class="doughnut-chart-row">
      <div class="chart-container" v-for="index in [2, 3]" :key="index">
        <canvas :ref="'doughnutChart' + index"></canvas>
      </div>
    </div>
    <div class="doughnut-chart-row">
      <!-- Adjusted ref for consistency -->
      <div class="chart-container" v-for="index in [4]" :key="index">
        <canvas :ref="'doughnutChart' + index"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export default {
  data() {
    return {
      barChart: null,
      doughnutCharts: [],
      doughnutChartData: [
        { correct: 300, incorrect: 200 },
        { correct: 280, incorrect: 220 },
        { correct: 150, incorrect: 350 },
        { correct: 400, incorrect: 100 },
        { correct: 350, incorrect: 150 },
      ],
    };
  },
  mounted() {
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
      this.doughnutChartData.forEach((data, index) => {
        this.$nextTick(() => {
          const context =
            this.$refs["doughnutChart" + index][0].getContext("2d");
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
                display: false, // Disable legend
              },
            },
          });
          this.doughnutCharts.push(chart);
        });
      });
    },
  },
};
</script>

<style scoped>
.doughnut-chart-row {
  display: flex;
  justify-content: center;
  margin-bottom: 20px; /* Space between rows */
}

.chart-container {
  flex: 0 1 50%; /* Flex-grow, flex-shrink, flex-basis */
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px; /* Optional: for spacing around charts */
}

/* Style for the bar chart container */
.bar-chart-container {
  margin-top: 20px; /* Optional: space above the bar chart */
}
</style>
