<!-- components/ChartComponent.vue not being used: expansion to different types of graphs -->
<template>
  <div>
    <!-- Radio buttons to switch chart types -->
    <div class="chart-switch-buttons">
      <label>
        <input
          type="radio"
          value="bar"
          v-model="currentChartType"
          name="chartType"
        />
        Bar
      </label>
      <label>
        <input
          type="radio"
          value="doughnut"
          v-model="currentChartType"
          name="chartType"
        />
        Doughnut
      </label>
      <label>
        <input
          type="radio"
          value="pie"
          v-model="currentChartType"
          name="chartType"
        />
        Pie
      </label>
      <label>
        <input
          type="radio"
          value="polarArea"
          v-model="currentChartType"
          name="chartType"
        />
        Polar Area
      </label>
    </div>

    <!-- Chart canvas -->
    <div class="chart-container">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export default {
  props: {
    data: Object,
    // Removed chartType prop since we use a data property instead
  },
  data() {
    return {
      chart: null,
      currentChartType: "bar", // Default chart type
    };
  },
  watch: {
    data: {
      handler(newData) {
        if (this.chart) {
          this.chart.data = newData;
          this.chart.update();
        }
      },
      deep: true,
    },
    currentChartType() {
      // This watcher is triggered when currentChartType changes
      this.createChart();
    },
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
      // Destroy the existing chart before creating a new one
      if (this.chart) {
        this.chart.destroy();
        this.chart = null;
      }
      this.$nextTick(() => {
        if (this.$refs.chartCanvas) {
          this.chart = new Chart(this.$refs.chartCanvas.getContext("2d"), {
            type: this.currentChartType,
            data: this.data || {}, // Fallback in case data is not provided
            options: {
              scales: {
                y: {
                  beginAtZero: true,
                  display:
                    this.currentChartType === "bar" ||
                    this.currentChartType === "line",
                },
              },
              responsive: true,
              maintainAspectRatio: false,
            },
          });
        }
      });
    },
    destroyChart() {
      if (this.chart) {
        this.chart.destroy();
        this.chart = null;
      }
    },
  },
};
</script>

<style scoped>
.chart-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 400px; /* Adjust height as needed */
}
.chart-switch-buttons button {
  margin: 5px;
  padding: 5px 10px;
}
</style>
