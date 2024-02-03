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
    shouldRenderChart: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      chart: null,
    };
  },
  mounted() {
    //console.log("OptionDistributionChart component mounted");
    if (this.shouldRenderChart) {
      this.createOrUpdateChart();
    }
  },
  watch: {
    optionDistributionData() {
      this.createOrUpdateChart();
    },
    shouldRenderChart(newVal) {
      if (newVal) {
        this.createCharts();
      } else {
        this.destroyCharts();
      }
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
      //console.log("Creating bar chart...");
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
        animation: false,
        maintainAspectRatio: false,
      };

      this.chart = new Chart(this.$refs.chart.getContext("2d"), {
        type: "bar",
        data: chartData,
        options: options,
      });
      //console.log("Option distribution chart created: ", this.chart);
    },
  },
};
</script>
