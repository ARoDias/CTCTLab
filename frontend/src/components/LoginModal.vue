<template>
  <!-- Utiliza o componente modal genérico -->
  <ModalComponent
    :isVisible="showModal"
    @update:isVisible="handleVisibilityChange"
  >
    <template #header>
      <!-- Conteúdo personalizado para o cabeçalho do modal -->
      <h5 class="modal-title">Login de Utilizador</h5>
    </template>

    <template #default>
      <!-- Corpo principal do modal, contendo o formulário de login -->
      <form @submit.prevent="submitLogin">
        <div class="form-group">
          <label for="username">Username (número de aluno):</label>
          <input
            type="text"
            id="username"
            v-model="username"
            autocomplete="username"
          />
        </div>
        <div class="form-group">
          <label for="password">Senha/Password:</label>
          <input
            type="password"
            id="password"
            v-model="password"
            autocomplete="current-password"
          />
        </div>
        <div class="submit-button">
          <button class="btn btn-primary" type="submit">Login</button>
        </div>
      </form>
      <div v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
      </div>
    </template>

    <template #footer>
      <!-- Conteúdo personalizado para o rodapé do modal, se necessário -->
    </template>
  </ModalComponent>
</template>

<script>
import axios from "axios";
import ModalComponent from "@/components/ModalComponent.vue";

export default {
  components: {
    ModalComponent,
  },
  data() {
    return {
      username: "",
      password: "",
      showModal: true,
      errorMessage: "",
    };
  },
  methods: {
    closeModal() {
      this.showModal = false;
      this.errorMessage = "";
      document.title = "CTCTLab";
      this.$emit("closeModal");
    },
    handleVisibilityChange(value) {
      this.showModal = value;
    },
    async submitLogin() {
      try {
        const response = await axios.post("/api/users/login/", {
          username: this.username,
          password: this.password,
        });

        const {
          key: token,
          user_type: userType,
          user_id: userId,
        } = response.data;
        if (token) {
          this.$store.dispatch("updateAuthToken", token);
          this.$store.dispatch("updateCurrentUser", {
            user: userId,
            userType: userType,
            username: this.username, // Assuming username is the student number for student users
          });
          this.$router.push("/");
          this.closeModal();
        } else {
          this.errorMessage =
            "Login falhou. Por favor, verifica as tuas credenciais.";
        }
      } catch (error) {
        this.errorMessage =
          "Ocorreu um erro ao fazer login. Por favor, tenta novamente.";
        console.error("Erro ao submeter o formulário de login:", error);
      }
    },
  },
  created() {
    document.title = "Login";
  },
};
</script>
