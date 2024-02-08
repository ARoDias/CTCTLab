<!--views/HomePage.vue -->
<template>
  <div>
    <main>
      <div class="container">
        <div class="language-selector">
          <button @click="setLanguage('PT')">PT</button>
          <button @click="setLanguage('EN')">EN</button>
        </div>
        <h2>{{ currentLanguage === "PT" ? "NOTÍCIAS" : "NEWS" }}</h2>
        <!-- A classe news-container deve envolver diretamente os NewsCard -->
        <div class="news-container">
          <!-- Iterate over the newsItems array to display each news card -->
          <NewsCard
            v-for="(newsItem, index) in newsItems"
            :key="index"
            :title="
              currentLanguage === 'PT' ? newsItem.titlePT : newsItem.titleEN
            "
            :content="
              currentLanguage === 'PT' ? newsItem.contentPT : newsItem.contentEN
            "
          />
        </div>
        <CourseProgram :currentLanguage="currentLanguage" />
      </div>
    </main>
  </div>
</template>

<script>
import NewsCard from "./NewsCard.vue";
import CourseProgram from "./CourseProgram.vue";
export default {
  components: {
    NewsCard,
    CourseProgram,
  },
  data() {
    return {
      currentLanguage: "PT",
      newsItems: [
        {
          titlePT:
            "22 jan 2024 - Lançamento da Semana de Planeamento Curricular para a Empregabilidade",
          contentPT:
            "A primeira semana marcou o início da jornada dos alunos em CTCT, focada no desenvolvimento de competências transversais essenciais, como a preparação de CVs e técnicas de entrevista. Os alunos participaram em atividades práticas e interativas, preparando-os para o mercado de trabalho.",
          titleEN: "Launch of the Curriculum Planning Week for Employability",
          contentEN:
            "The first week marked the beginning of the students' journey in CTCT, focusing on the development of essential transversal skills such as CV preparation and interview techniques. Students engaged in practical and interactive activities, preparing them for the job market.",
        },
        {
          titlePT:
            "29 jan 2024 - Lançamento da Semana: Gestão do Tempo, Trabalho em Equipa e Liderança",
          contentPT:
            "A segunda semana do CTCT aprofundou a gestão do tempo, trabalho em equipa e liderança. Os alunos mergulharam em atividades práticas como 'O Painel da Maria' e simulações de liderança, enfatizando a importância dos objetivos SMART e da comunicação eficaz dentro das equipas.",
          titleEN: "Week Highlight: Time Management, Teamwork, and Leadership",
          contentEN:
            "The second week of CTCT delved into time management, teamwork, and leadership. Students immersed in practical activities like 'Maria's Panel' and leadership simulations, emphasizing the importance of SMART goals and effective communication within teams.",
        },
        {
          titlePT:
            "5 fev 2024 - Lançamento da Semana Dedicada à Gestão de Informação e Comunicação",
          contentPT:
            "Na terceira semana, CTCT centrou-se na Gestão de Informação e Comunicação, abordando desde a instalação do Mendeley Reference Manager até à comunicação eficaz em Ciência e Tecnologia. Os alunos exploraram a ética e a deontologia na pesquisa, preparando-os para desafios reais.",
          titleEN: "Advances in Information Management and Communication",
          contentEN:
            "In the third week, CTCT focused on Information Management and Communication, from installing Mendeley Reference Manager to effective communication in Science and Technology. Students explored ethics and deontology in research, preparing them for real-world challenges.",
        },
      ],
    };
  },
  methods: {
    setLanguage(lang) {
      this.currentLanguage = lang;
    },
  },
};
</script>

<style scoped>
.language-selector {
  display: flex;
  justify-content: flex-end;
  padding: 10px;
}

.language-selector button {
  padding: 5px 10px;
  margin-left: 5px;
  cursor: pointer;
  background-color: var(--primary-blue);
  color: var(--white);
  border: none;
  border-radius: var(--border-radius);
  outline: none;
}

.language-selector button:focus {
  box-shadow: 0 0 0 2px var(--secondary-blue);
}

.language-selector button.active {
  background-color: var(--secondary-blue);
}

h2 {
  color: var(--white);
  text-align: center;
  margin-bottom: 20px;
}
.news-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

/* Não precisa de .news-card aqui, pois já está estilizado no componente NewsCard.vue */

@media (min-width: 768px) {
  /* Para dispositivos maiores, como tablets e desktops */
  .news-card {
    /* Ajuste para que não ocupe mais do que um terço do container, menos o espaço do gap */
    flex-basis: calc(33.333% - 20px);
  }
}

@media (max-width: 767px) {
  /* Para dispositivos menores, como telefones */
  .news-card {
    /* Cartões devem ocupar toda a largura disponível */
    flex-basis: 100%;
  }
}
</style>
