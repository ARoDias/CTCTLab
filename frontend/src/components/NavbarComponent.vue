<template>
  <!-- Main navigation bar of the application -->
  <nav class="navbar navbar-expand-lg">
    <div class="container">
      <!-- Logo and link to the home page -->
      <router-link to="/" class="navbar-brand">
        <img :src="logoURL" alt="Logo" />
      </router-link>

      <!-- Button for toggling navigation bar in smaller screens -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navigation links -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <!-- Dynamically display week links if user is authenticated -->
          <template v-if="userAuthenticated">
            <li class="nav-item" v-for="week in weeks" :key="week.id">
              <router-link :to="week.url" class="nav-link fs-6">{{
                week.name
              }}</router-link>
            </li>
            <!-- New link for TP Classes page (to be created) -->
            <li class="nav-item">
              <router-link to="/tp-classes" class="nav-link fs-6"
                >Aulas TP</router-link
              >
            </li>
          </template>
        </ul>
      </div>

      <!-- Authentication related links -->
      <div>
        <a v-if="!userAuthenticated" href="#" @click="navigateToRegister"
          >REGISTAR</a
        >
        <a v-if="!userAuthenticated" href="#" @click="navigateToLogin">LOGIN</a>
        <a v-if="userAuthenticated" href="#" @click="logout">SAIR</a>
        <!-- Registration and Login modals -->
        <RegisterModal
          v-if="showModal && currentModalType === 'register'"
          @closeModal="closeModal"
        ></RegisterModal>
        <LoginModal
          v-if="showModal && currentModalType === 'login'"
          @closeModal="closeModal"
        ></LoginModal>
      </div>
    </div>
  </nav>
</template>

<script>
import LoginModal from "./LoginModal.vue";
import RegisterModal from "./RegisterModal.vue";

export default {
  components: {
    LoginModal,
    RegisterModal,
  },
  data() {
    return {
      logoURL: require("@/assets/logo_ctct.png"),
      weeks: [
        { id: 1, name: "Semana 1", url: "/week/1" },
        { id: 2, name: "Semana 2", url: "/week/2" },
        { id: 3, name: "Semana 3", url: "/week/3" },
        { id: 4, name: "Semana 4", url: "/week/4" },
      ],
      showModal: false,
      currentModalType: "",
    };
  },
  computed: {
    // Computed property to check if the user is authenticated
    userAuthenticated() {
      return this.$store.getters.isLoggedIn;
    },
  },
  methods: {
    // Method to log out the user
    logout() {
      //console.log("Logout feito no NavbarComponent");
      this.$store.dispatch("logout");
      this.$emit("logout");
    },
    // Method to navigate to the login modal
    navigateToLogin() {
      this.openModal("login");
    },
    // Method to navigate to the registration modal
    navigateToRegister() {
      this.openModal("register");
    },
    // Method to open a modal
    openModal(modalType) {
      this.currentModalType = modalType;
      this.showModal = true;
    },
    // Method to close the current modal
    closeModal() {
      this.showModal = false;
    },
  },
};
</script>
