<template>
  <!-- Root element of the Vue application -->
  <div id="app">
    <!-- Application header section containing the title and navigation bar -->
    <header>
      <!-- Meta tags for responsive design and character encoding -->
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>CTCTLab</title>

      <!-- Main title of the application -->
      <h1 style="text-align: center">
        Competências Transversais para Ciências e Tecnologia
      </h1>

      <!-- Navigation bar component, listening to the logout event -->
      <NavbarComponent @logout="logOut"></NavbarComponent>
    </header>

    <!-- Main content area of the application, where router-view will display the component based on the route -->
    <main>
      <router-view></router-view>
    </main>

    <!-- Footer section of the application -->
    <footer>
      <div class="container">
        <!-- Footer text with copyright information -->
        <p>CTCT &copy; 2023/2024</p>
      </div>
    </footer>
  </div>
</template>

<script>
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "App",
  components: {
    NavbarComponent,
  },
  computed: {
    currentUser() {
      return this.$store.getters.getCurrentUser;
    },
    loggedIn() {
      return this.$store.getters.isLoggedIn;
    },
  },
  created() {
    if (this.loggedIn) {
      this.fetchCurrentUser();
    }
  },
  methods: {
    fetchCurrentUser() {
      const token = this.$store.getters.getAuthToken;
      if (token) {
        this.$axios
          .get("/api/users/currentUser", {
            headers: { Authorization: `Bearer ${token}` },
          })
          .then((response) => {
            this.$store.dispatch("updateCurrentUser", response.data);
          })
          .catch((error) => {
            console.error("Error fetching user data:", error);
            //console.log("Logout feito na App catch error");
            this.$store.dispatch("logout");
            this.$router.push("/login");
          });
      } else {
        //console.log("Logout feito na App else");
        this.$store.dispatch("logout");
      }
    },
    logOut() {
      //console.log("Logout feito na App");
      this.$store.dispatch("logout");
      this.$router.push("/login");
    },
  },
};
</script>

<!-- Importing external CSS file for styling -->
<style>
@import url("assets/style.css");
</style>
