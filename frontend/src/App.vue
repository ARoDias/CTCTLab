<template>
  <!-- Root element of the Vue application -->
  <div id="app">
    <!-- Application header section containing the title and navigation bar -->
    <header>
      <!-- Meta tags for responsive design and character encoding -->
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>CTCTOnlineHub</title>

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
  data() {
    return {
      currentUser: null, // Current user's data
      tasks: [], // Task data for the user
      loggedIn: false, // Boolean to track if the user is logged in
      home: true, // Boolean to determine if the home page should be displayed
      week: 1, // Current week number for display
    };
  },
  mounted() {
    // Fetch user and tasks data when the component is mounted
    this.fetchCurrentUser();
    this.fetchTasks();
  },
  methods: {
    fetchCurrentUser() {
      // Retrieve the JWT token from localStorage
      const token = localStorage.getItem("userToken");
      if (token) {
        // If token exists, fetch the current user's data from the API
        this.$axios
          .get("/api/users/currentUser", {
            headers: { Authorization: `Bearer ${token}` },
          })
          .then((response) => {
            this.currentUser = response.data;
            this.loggedIn = true;
          })
          .catch((error) => {
            console.error("Error fetching user data:", error);
            this.loggedIn = false;
          });
      } else {
        console.log("User is not logged in.");
        this.loggedIn = false;
      }
    },
    fetchTasks() {
      const token = localStorage.getItem("userToken");
      if (token) {
        // If token exists, fetch tasks from the API
        this.$axios
          .get("/api/questions/tasks/", {
            headers: { Authorization: `Bearer ${token}` },
          })
          .then((response) => {
            this.tasks = response.data;
            this.loggedIn = true;
          })
          .catch((error) => {
            console.error("Error fetching tasks data:", error);
            this.loggedIn = false;
          });
      } else {
        console.log("User is not logged in.");
        this.loggedIn = false;
      }
    },
    logOut() {
      // Log out the user by resetting relevant data properties
      this.loggedIn = false;
      this.currentUser = null;
      localStorage.removeItem("userToken"); // Remove the token from localStorage
      this.$emit("logout"); // Emit a logout event to inform other components
    },
    logIn(user) {
      // Log in the user by setting the currentUser and loggedIn properties
      this.loggedIn = true;
      this.currentUser = user;
      // Additional login operations can be performed here
    },
  },
};
</script>

<!-- Importing external CSS file for styling -->
<style>
@import url("assets/style.css");
</style>
