<template>
  <div>
    <!-- Botão para abrir o questionário -->
    <button @click="fetchQuestionnaire">Abrir Questionário</button>

    <!-- Modal para mostrar as perguntas -->
    <QuestionsModal
      :show="showModal"
      @close="closeModal"
      :title="questionnaireTitle"
    >
      <!-- Header do modal com o título do questionário -->
      <template v-slot:header>
        <h3>{{ questionnaireTitle }}</h3>
      </template>

      <!-- Renderiza o componente de perguntas ou de resultados com base no estado -->
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
      questionnaireTitle: "",
      results: [
        // Configuração dos resultados
      ],
    };
  },
  methods: {
    // Busca os detalhes do questionário quando o componente é criado
    fetchQuestionnaire() {
      axios
        .get("http://127.0.0.1:8000/api/questions/questionnaires/2/")
        .then((response) => {
          this.questionnaireTitle = response.data.title;
          this.fetchQuestions(response.data.questions);
        })
        .catch((error) => {
          console.error("Erro ao carregar o questionário", error);
        });
    },
    // Carrega as perguntas com base nos IDs fornecidos pelo questionário
    fetchQuestions(questionIds) {
      const requests = questionIds.map((id) =>
        axios.get(`http://127.0.0.1:8000/api/questions/questions/${id}`)
      );

      Promise.all(requests)
        .then((responses) => {
          this.questions = responses.map((res) => res.data);
          this.showModal = true; // Mostra o modal com as perguntas imediatamente
        })
        .catch((error) => {
          console.error("Erro ao carregar perguntas", error);
        });
    },
    closeModal() {
      // Reseta o estado e fecha o modal
      this.showModal = false;
      this.reset();
    },
    questionAnswered(isCorrect) {
      // Trata o evento quando uma resposta é selecionada
      if (isCorrect) {
        this.totalCorrect++;
      }
      this.questionsAnswered++;
      if (this.questionsAnswered >= this.questions.length) {
        this.showModal = false; // Fecha o modal quando todas as perguntas forem respondidas
      }
    },
    reset() {
      // Reseta o estado do questionário
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
</style>
