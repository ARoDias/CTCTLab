<!-- components/OptionDistributionChart.vue -->
<template>
  <div class="chart-container">
    <canvas ref="chart"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
import apiClient from "@/axiosConfig";
Chart.register(...registerables);

export default {
  props: {
    questionIds: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      chart: null,
      optionDistributionData: [],
    };
  },
  async mounted() {
    await this.fetchOptionDistribution();
    this.createChart();
  },
  beforeUnmount() {
    if (this.chart) {
      console.log("Destroying option distribution chart: ", this.chart);
      this.chart.destroy();
    }
  },
  methods: {
    async fetchOptionDistribution() {
      try {
        const response = await apiClient.get("/api/questions/opt_dist/", {
          params: { question_ids: this.questionIds.join(",") },
        });
        this.optionDistributionData = response.data;
      } catch (error) {
        console.error("Error fetching option distribution data:", error);
      }
    },
    createChart() {
      if (this.chart) {
        console.log("Destroying old option distribution chart");
        this.chart.destroy();
      }

      const labels = this.optionDistributionData.map(
        (data) => `Q${data.question_id}`
      );
      const datasets = this.optionDistributionData.map((data) => ({
        label: `Question ${data.question_id}`,
        backgroundColor: this.getRandomColor(),
        data: data.distribution.map((opt) => opt.count),
      }));

      const chartData = { labels, datasets };
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
        data: chartData,
        options: options,
      });
      console.log("Creating option distribution chart");
    },
    getRandomColor() {
      // Esta função gera uma cor aleatória.
      // Você pode querer ajustar isso para ter um conjunto fixo de cores.
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
