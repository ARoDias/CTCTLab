<!-- components/NotFound.vue -->
<template>
  <div class="card">
    <img
      :src="notFoundpict"
      alt="Página não encontrada - Not Found Error 404"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      notFoundpict: require("@/assets/404-error-with-cute-animal-concept-illustration.jpg"),
    };
  },
};
</script>
