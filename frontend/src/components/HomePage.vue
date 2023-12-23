<!--views/HomePage.vue -->
<template>
  <div>
    <main>
      <div class="container">
        <div class="row">
          <div class="column">
            <h2>Notícias</h2>
            <div class="card-container">
              <NewsCard :title="title" :content="content1"></NewsCard>
            </div>
          </div>
          <br /><br />
          <div class="column">
            <CourseProgram />
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
      title: "Início das Aulas",
      content1: "Dia 22 de Janeiro começam as aulas...",
    };
  },
};
</script>

<style scoped>
h2 {
  color: var(--white);
}
</style>
