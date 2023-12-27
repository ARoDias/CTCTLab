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
    // Computed properties to access the state from the Vuex store
    currentUser() {
      return this.$store.getters.getCurrentUser;
    },
    loggedIn() {
      return this.$store.getters.isLoggedIn;
    },
    tasks() {
      // Assuming you have a getter for tasks in your store
      return this.$store.getters.getTasks;
    },
  },
  created() {
    // Check if the user is already logged in when the component is created
    this.checkLoginStatus();
  },
  methods: {
    checkLoginStatus() {
      // Check if the user is logged in using Vuex getters
      if (this.loggedIn) {
        this.fetchCurrentUser();
        this.fetchTasks();
      }
    },
    fetchCurrentUser() {
      // Use the token from Vuex store for API requests
      const token = this.$store.getters.getAuthToken;
      if (token) {
        // Fetch the current user's data from the API
        this.$axios
          .get("/api/users/currentUser", {
            headers: { Authorization: `Bearer ${token}` },
          })
          .then((response) => {
            // Update Vuex store with the current user's data
            this.$store.dispatch("updateCurrentUser", response.data);
          })
          .catch((error) => {
            console.error("Error fetching user data:", error);
            // Handle error, for example by redirecting to login
          });
      }
    },
    fetchTasks() {
      // Use the token from Vuex store for API requests
      const token = this.$store.getters.getAuthToken;
      if (token) {
        // Fetch tasks from the API
        this.$axios
          .get("/api/questions/tasks/", {
            headers: { Authorization: `Bearer ${token}` },
          })
          .then((response) => {
            // Update Vuex store with the tasks data
            this.$store.dispatch("updateTasks", response.data);
          })
          .catch((error) => {
            console.error("Error fetching tasks data:", error);
            // Handle error, for example by showing a message to the user
          });
      }
    },
    logOut() {
      // Use Vuex action to log out the user
      this.$store.dispatch("logout");
      // Redirect to the login page or home page as needed
      this.$router.push("/login");
    },
  },
};
</script>

<!-- Importing external CSS file for styling -->
<style>
@import url("assets/style.css");
</style>
