<!-- components/NewsCard.vue -->
<template>
  <div class="card">
      <h3>{{ title }}</h3>
      <div v-html="content"></div>
  </div>
</template>

<script>
export default {
  props: {
      title: String,
      content: String
  }
}
</script>
