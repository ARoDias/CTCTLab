<template>
  <div>
    <!-- Button to open the questions modal -->
    <button @click="showModal = true">Abrir Questionário</button>

    <!-- QuestionsModal with the content passed as slot -->
    <QuestionsModal :show="showModal" @close="closeModal">
      <QuestionsComponent
        v-if="questionsAnswered < questions.length"
        :question="questions[questionsAnswered]"
        @question-answered="questionAnswered"
      />
      <ResultComponent v-else :result="results[totalCorrect]" />
    </QuestionsModal>
  </div>
</template>

<script>
import QuestionsModal from '@/components/QuestionsModal.vue';
import QuestionsComponent from '@/components/QuestionsComponent.vue';
import ResultComponent from '@/components/ResultComponent.vue';

export default {
  components: {
    QuestionsModal,
    QuestionsComponent,
    ResultComponent,
  },
  data() {
    return {
      showModal: false,
      questionsAnswered: 0,
        totalCorrect: 0,
        questions: [
          {
            q: "What is 2 + 2?",
            answers: [
              {
                text: "4",
                is_correct: true,
              },
              {
                text: "3",
                is_correct: false,
              },
              {
                text: "Fish",
                is_correct: false,
              },
              {
                text: "5",
                is_correct: false,
              },
            ],
          },
          {
            q: 'How many letters are in the word "Banana"?',
            answers: [
              {
                text: "5",
                is_correct: false,
              },
              {
                text: "7",
                is_correct: false,
              },
              {
                text: "6",
                is_correct: true,
              },
              {
                text: "12",
                is_correct: false,
              },
            ],
          },
          {
            q: "Find the missing letter: C_ke",
            answers: [
              {
                text: "e",
                is_correct: false,
              },
              {
                text: "a",
                is_correct: true,
              },
              {
                text: "i",
                is_correct: false,
              },
            ],
          },
        ],
        results: [
          {
            min: 0,
            max: 2,
            title: "Try again!",
            desc: "Do a little more studying and you may succeed!",
          },
          {
            min: 3,
            max: 3,
            title: "Wow, you're a genius!",
            desc: "Studying has definitely paid off for you!",
          },
        ],
      };
    },
  methods: {
    closeModal() {
      this.showModal = false;
    },
    questionAnswered(isCorrect) {
      if (isCorrect) {
        this.totalCorrect++;
      }
      if (this.questionsAnswered < this.questions.length - 1) {
        this.questionsAnswered++;
      } else {
        // Close the modal after the last question
        this.showModal = false;
      }
    },
      reset() {
        this.questionsAnswered = 0;
        this.totalCorrect = 0;
      },
  },
};
</script>
