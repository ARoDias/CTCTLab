<!-- components/QuestionsComponent.vue -->
<template>
  <div class="questions-ctr">
    <div class="question">{{ question.question_text }}</div>
    <div class="answers">
      <button
        v-for="option in question.options"
        :key="option.id"
        @click="selectAnswer(question.id, option.id)"
        class="answer"
      >
        {{ option.option_text }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: ["question"],
  emits: ["question-answered"],
  methods: {
    selectAnswer(questionId, selectedOptionId) {
      this.$emit("question-answered", questionId, selectedOptionId);
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
  padding: 10px;
  font-size: 22px;
  font-weight: bold;
  text-align: center;
  background-color: var(--primary-green);
  color: var(--white);
  box-sizing: border-box;
}
/* Styles for question options */
.answer {
  border: 1px solid var(--secondary-blue);
  padding: 10px;
  font-size: 18px;
  width: 100%;
  background-color: var(--white);
  color: var(--black);
  transition: background-color 0.1s, color 0.1s;
}

/* Hover effect for question options */
.answer:hover {
  background-color: var(--white);
  color: var(--primary-blue);
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
  background-color: var(--secondary-blue);
  border-color: var(--primary-green);
  color: var(--white);
}
</style>
