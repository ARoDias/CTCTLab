<!-- components/ResultsGraph.vue -->
<template>
  <div>
    <!-- Buttons to switch between graphs -->
    <div class="graph-switch">
      <button @click="currentGraph = 'correctIncorrect'">
        Correct/Incorrect
      </button>
      <button @click="currentGraph = 'distribution'">
        Option Distribution
      </button>
    </div>

    <!-- Conditionally render the chart components -->
    <CorrectIncorrectChart
      v-show="currentGraph === 'correctIncorrect'"
      :question-ids="questionIds"
    />
    <OptionDistributionChart
      v-show="currentGraph === 'distribution'"
      :question-ids="questionIds"
    />
  </div>
</template>

<script>
import CorrectIncorrectChart from "./CorrectIncorrectChart.vue";
import OptionDistributionChart from "./OptionDistributionChart.vue";

export default {
  components: {
    CorrectIncorrectChart,
    OptionDistributionChart,
  },
  props: {
    questionIds: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      currentGraph: "correctIncorrect",
    };
  },
};
</script>

<style>
.graph-switch button {
  margin: 10px;
  padding: 5px 15px;
  border: 1px solid #ccc;
  background-color: #fff;
  cursor: pointer;
}
.graph-switch button:focus {
  outline: none;
  border-color: #446ebc;
}
/* No need for .chart-container style here, as it will be in the child components */
</style>
