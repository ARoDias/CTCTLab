<template>
  <div>
    <button @click="fetchQuestions">Abrir Questionário</button>

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
import axios from "axios";
import QuestionsModal from "@/components/QuestionsModal.vue";
import QuestionsComponent from "@/components/QuestionsComponent.vue";
import ResultComponent from "@/components/ResultComponent.vue";

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
      questions: [],
      results: [
        {
          min: 0,
          max: 2,
          title: "Tente novamente!",
          desc: "Estude um pouco mais e poderá ter sucesso!",
        },
        {
          min: 3,
          max: 3,
          title: "Uau, você é um génio!",
          desc: "O estudo definitivamente compensou para você!",
        },
      ],
    };
  },
  methods: {
    fetchQuestions() {
      axios
        .get("http://127.0.0.1:8000/api/questions/questionnaires/2/")
        .then((response) => {
          const questionnaireId = response.data.questions;
          this.loadQuestions(questionnaireId);
          this.showModal = true;
        })
        .catch((error) => {
          console.error("Erro ao carregar o questionário", error);
        });
    },
    loadQuestions(questionnaireId) {
      axios
        .get(
          `http://127.0.0.1:8000/api/questions/questions/?questionnaire=${questionnaireId}`
        )
        .then((response) => {
          this.questions = response.data.map((q) => ({
            q: q.question_text,
            answers: q.options,
          }));
        })
        .catch((error) => {
          console.error("Erro ao carregar perguntas", error);
        });
    },
    closeModal() {
      this.showModal = false;
      this.reset();
    },
    questionAnswered(isCorrect) {
      if (isCorrect) {
        this.totalCorrect++;
      }
      this.questionsAnswered++;
      if (this.questionsAnswered >= this.questions.length) {
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

.ctr {
  margin: 0 auto;
  max-width: 600px;
  width: 100%;
  box-sizing: border-box;
  position: relative;
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
.single-question {
  position: relative;
  width: 100%;
}
.answer {
  border: 1px solid #8e959f;
  padding: 20px;
  font-size: 18px;
  width: 100%;
  background-color: #fff;
  transition: 0.2s linear all;
}
.answer span {
  display: inline-block;
  margin-left: 5px;
  font-size: 0.75em;
  font-style: italic;
}
.progress {
  height: 50px;
  margin-top: 10px;
  background-color: #ddd;
  position: relative;
}
.bar {
  height: 50px;
  background-color: #ff6372;
  transition: all 0.3s linear;
}
.status {
  position: absolute;
  top: 15px;
  left: 0;
  text-align: center;
  color: #fff;
  width: 100%;
}
.answer:not(.is-answered) {
  cursor: pointer;
}
.answer:not(.is-answered):hover {
  background-color: #8ce200;
  border-color: #8ce200;
  color: #fff;
}

.title {
  width: 100%;
  padding: 20px;
  font-size: 32px;
  font-weight: bold;
  text-align: center;
  background-color: #12cbc4;
  color: #fff;
  box-sizing: border-box;
}
.desc {
  border: 1px solid #8e959f;
  padding: 20px;
  font-size: 18px;
  width: 100%;
  background-color: #fff;
  transition: 0.4s linear all;
  text-align: center;
}
.fade-enter-from {
  opacity: 0;
}
.fade-enter-active {
  transition: all 0.3s linear;
}
.fade-leave-active {
  transition: all 0.3s linear;
  opacity: 0;
  position: absolute;
}
.fade-leave-to {
  opacity: 0;
}

.reset-btn {
  background-color: #ff6372;
  border: 0;
  font-size: 22px;
  color: #fff;
  padding: 10px 25px;
  margin: 10px auto;
  display: block;
}

.result {
  width: 100%;
}

.reset-btn:active,
.reset-btn:focus,
.reset-btn:hover {
  border: 0;
  outline: 0;
}
</style>
