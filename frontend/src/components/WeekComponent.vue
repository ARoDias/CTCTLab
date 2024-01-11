<!-- components/WeekComponent.vue -->

<!-- The template for the WeekComponent -->
<template>
  <div>
    <h2>{{ title }}</h2>
    <div v-if="currentUser && currentUser.role === 'teacher'">
      <p>Verificar que está a funcionar... docente</p>
      <!-- Teacher-specific content -->
    </div>
    <div v-else>
      <p>Verificar que está a funcionar... aluno</p>
      <!-- Loop through activities and display them -->
      <!-- <div v-for="activity in activities" :key="activity.id">
        <h3>{{ activity.title }}</h3>
        <p>{{ activity.description }}</p>
        <p>Verificar que está a funcionar...</p>
         Outras informações da atividade 
     </div>  -->
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: ["weekNumber"],
  data() {
    return {
      title: "",
      activities: [],
    };
  },
  computed: {
    currentUser() {
      return this.$store.getters.getCurrentUser;
    },
  },
  created() {
    this.fetchActivities();
    console.log(this.$route.params.weekNumber);
  },
  watch: {
    "$route.params.weekNumber": "fetchActivities",
  },
  methods: {
    fetchActivities() {
      this.title = `Semana ${this.$route.params.weekNumber}`;
      axios
        .get(`/api/questions/activity?week=${this.$route.params.weekNumber}`)
        .then((response) => {
          this.activities = response.data;
        })
        .catch((error) => {
          console.error("Erro ao buscar atividades:", error);
        });
    },
  },
};
</script>

<style scoped>
h2 {
  color: var(--white);
}
</style>
