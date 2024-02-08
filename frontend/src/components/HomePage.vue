<!--views/HomePage.vue -->
<template>
  <div>
    <main>
      <div class="container">
        <div class="language-selector">
          <button @click="setLanguage('PT')">PT</button>
          <button @click="setLanguage('EN')">EN</button>
        </div>
        <div class="row">
          <div class="column">
            <h2 v-if="currentLanguage === 'PT'">NOTÍCIAS</h2>
            <h2 v-if="currentLanguage === 'EN'">NEWS</h2>
            <div class="card-container">
              <!-- Pass the currentLanguage to the NewsCard component -->
              <NewsCard
                :title="currentLanguage === 'PT' ? titlePT : titleEN"
                :content="currentLanguage === 'PT' ? content1PT : content1EN"
              ></NewsCard>
            </div>
          </div>
          <br /><br />
          <div class="column">
            <!-- Pass the currentLanguage to the CourseProgram component -->
            <CourseProgram :currentLanguage="currentLanguage" />
          </div>
        </div>
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
      titlePT: "Início das Aulas",
      content1PT: "Dia 22 de Janeiro começam as aulas...",
      titleEN: "Start of Classes",
      content1EN: "Classes start on January 22nd...",
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
/* Styles for the language selector */
.language-selector {
  text-align: right;
  padding: 10px;
}

/* Styles for the language switch buttons */
.language-selector button {
  padding: 5px 10px;
  margin-left: 5px;
  cursor: pointer;
  background-color: var(--primary-blue);
  color: var(--white);
  border: none;
  border-radius: var(--border-radius);
}

/* Styles for the language switch button when it is active */
.language-selector button.active {
  background-color: var(--secondary-blue);
}

h2 {
  color: var(--white);
}
</style>
