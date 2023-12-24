<!--  components/QuestionComponent.vue -->
<template>
  <div class="questions-ctr">
    <!-- Display the current question text -->
    <div class="question">{{ question.question_text }}</div>
    <div class="answers">
      <!-- Display all options for the current question -->
      <button
        v-for="option in question.options"
        :key="option.id"
        @click="selectAnswer(option.is_correct)"
        class="answer"
      >
        {{ option.option_text }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: ["question"], // Receives the current question object
  emits: ["question-answered"], // Emits an event when an answer is selected
  methods: {
    selectAnswer(isCorrect) {
      // Emit the event with the correctness of the selected option
      this.$emit("question-answered", isCorrect);
    },
  },
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}
body {
  font-size: 20px;
  font-family: sans-serif;
  padding-top: 20px;
  background: #e6ecf1;
}

.questions-ctr {
  position: relative;
  width: 100%;
}
.question {
  width: 100%;
  padding: 20px;
  font-size: 32px;
  font-weight: bold;
  text-align: center;
  background-color: #00ca8c;
  color: #fff;
  box-sizing: border-box;
}
/* Styles for question options */
.answer {
  border: 1px solid #8e959f;
  padding: 20px;
  font-size: 18px;
  width: 100%;
  background-color: #fff;
  color: #000; /* Text color black */
  transition: background-color 0.2s, color 0.2s;
}

/* Hover effect for question options */
.answer:hover {
  background-color: #e6ecf1; /* Light grey background on hover */
  color: #446ebc; /* Primary blue text color on hover */
}

.answer span {
  display: inline-block;
  margin-left: 5px;
  font-size: 0.75em;
  font-style: italic;
}

.answer:not(.is-answered) {
  cursor: pointer;
}
.answer:not(.is-answered):hover {
  background-color: #8ce200;
  border-color: #8ce200;
  color: #fff;
}
</style>
