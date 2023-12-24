<template>
  <div class="result" v-if="resultIndex !== null">
    <div class="title">{{ results[resultIndex].title }}</div>
    <div class="desc">{{ results[resultIndex].desc }}</div>
  </div>
</template>

<script>
export default {
  props: ["results", "totalCorrect"],
  computed: {
    resultIndex() {
      if (!this.results || this.results.length === 0) {
        return null;
      }

      let index = null;
      this.results.forEach((e, i) => {
        if (e.min <= this.totalCorrect && e.max >= this.totalCorrect) {
          index = i;
        }
      });

      return index;
    },
  },
};
</script>
