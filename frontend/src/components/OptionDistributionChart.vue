<!-- components/OptionDistributionChart.vue -->
<template>
  <div class="chart-container">
    <canvas ref="chart"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export default {
  data() {
    return {
      chart: null,
      optionDistributionData: [
        [50, 75, 150, 100, 25],
        [30, 120, 90, 60, 100],
        [80, 60, 40, 220, 100],
        [65, 85, 110, 45, 195],
        [45, 135, 65, 155, 100],
      ],
    };
  },
  mounted() {
    this.createChart();
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy();
    }
  },
  methods: {
    createChart() {
      const labels = ["A", "B", "C", "D", "E"];
      const datasets = this.optionDistributionData.map((data, index) => ({
        label: `Q${index + 1} Options`,
        backgroundColor: this.getRandomColor(),
        data,
      }));
      const data = { labels, datasets };
      const options = {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
        responsive: true,
        maintainAspectRatio: false,
      };
      this.chart = new Chart(this.$refs.chart.getContext("2d"), {
        type: "bar",
        data: data,
        options: options,
      });
    },
    getRandomColor() {
      return `#${Math.floor(Math.random() * 16777215).toString(16)}`;
    },
  },
};
</script>

<style scoped>
.chart-container {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
