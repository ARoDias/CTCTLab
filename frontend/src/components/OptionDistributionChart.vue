<!-- components/OptionDistributionChart.vue -->
<template>
  <div class="chart-container">
    <canvas ref="chart"></canvas>
  </div>

  <!-- Slot for inserting custom content from the parent component -->
  <slot></slot>
</template>

<script>
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

export default {
  props: {
    optionDistributionData: Array,
    questionDetails: Array,
  },
  data() {
    return {
      chart: null,
    };
  },
  mounted() {
    this.createOrUpdateChart();
  },
  watch: {
    optionDistributionData() {
      this.createOrUpdateChart();
    },
  },
  methods: {
    createOrUpdateChart() {
      if (this.chart) {
        // Destroy the old chart if it exists
        this.chart.destroy();
      }
      this.createChart();
    },
    createChart() {
      if (!this.optionDistributionData || !this.optionDistributionData.length) {
        console.log("No data for chart");
        return;
      }

      const labels = this.optionDistributionData.map(
        (data) => `Opção ${data.question_id}`
      );
      const datasets = this.optionDistributionData.map((data) => ({
        label: `Q${data.question_id}`,
        backgroundColor: data.backgroundColor,
        data: data.distribution,
      }));

      const chartData = { labels, datasets };
      const options = {
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 1, // Ensures only integers are used as step values
            },
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
      console.log("Option distribution chart created");
    },
  },
};
</script>
