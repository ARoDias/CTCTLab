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
        <canvas :ref="'doughnutChart' + index"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export default {
  props: {
    doughnutChartData: Array,
    questionDetails: Array,
  },
  data() {
    return {
      barChart: null,
      doughnutCharts: [],
    };
  },
  mounted() {
    if (this.doughnutChartData && this.doughnutChartData.length) {
      this.createCharts();
    }
  },
  beforeUnmount() {
    this.destroyCharts();
  },
  watch: {
    doughnutChartData(newData) {
      if (newData && newData.length) {
        this.updateCharts();
      }
    },
  },
  methods: {
    createCharts() {
      this.createBarChart();
      this.createDoughnutCharts();
    },
    updateCharts() {
      this.destroyCharts();
      this.createCharts();
    },
    createBarChart() {
      if (this.barChart) {
        console.log("Destroying old bar chart");
        this.barChart.destroy();
      }
      const barData = {
        labels: ["Q1", "Q2", "Q3", "Q4", "Q5"],
        datasets: [
          {
            label: "Respostas Certas",
            backgroundColor: "green",
            data: this.doughnutChartData.map((d) => d.correct),
          },
          {
            label: "Respostas Erradas",
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
      console.log("Creating bar chart");
    },
    createDoughnutCharts() {
      this.doughnutCharts.forEach((chart, index) => {
        if (chart) {
          console.log(`Destroying old doughnut chart ${index}`);
          chart.destroy();
        }
      });
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
              labels: ["Correcta", "Incorrecta"],
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
        console.log("Creating doughnut chart ${index}");
      });
    },

    destroyCharts() {
      if (this.barChart) {
        console.log("Destroying bar chart: ", this.barChart);
        this.barChart.destroy();
        this.barChart = null;
      }
      this.doughnutCharts.forEach((chart, index) => {
        if (chart) {
          console.log(`Destroying doughnut chart ${index}:`, chart);
          chart.destroy();
        }
      });
      this.doughnutCharts = [];
    },
  },
};
</script>
