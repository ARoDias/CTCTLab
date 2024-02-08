<!-- components/NewsCard.vue -->
<template>
  <div class="news-card">
    <h3>{{ title }}</h3>
    <div v-html="content"></div>
  </div>
</template>

<script>
export default {
  props: {
    title: String,
    content: String,
  },
};
</script>

<style scoped>
.news-card {
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 20px; /* Espaço abaixo de cada cartão */
  padding: 15px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

h3 {
  color: var(--primary-blue);
  text-align: center;
}

/* Responsividade não é necessária aqui, será controlada pelo container pai */
</style>
