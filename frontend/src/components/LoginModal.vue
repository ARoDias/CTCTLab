<template>
  <div class="modal" v-if="showModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Login de Utilizador</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            @click="closeModal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitLogin">
            <label for="username">Username (número de aluno):</label>
            <input
              type="text"
              id="username"
              v-model="username"
              autocomplete="username"
            />
            <label for="password">Senha/Password:</label>
            <input
              type="password"
              id="password"
              v-model="password"
              autocomplete="current-password"
            />
            <button class="btn btn-primary" type="submit">Login</button>
          </form>
          <div v-if="errorMessage" class="alert alert-danger">
            {{ errorMessage }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: "",
      showModal: true,
      errorMessage: "", // Mensagem de erro
    };
  },
  methods: {
    closeModal() {
      this.showModal = false;
      this.errorMessage = ""; // Limpar mensagem de erro ao fechar modal
      document.title = "CTCTLab";
      this.$emit("closeModal");
    },
    async submitLogin() {
      try {
        const response = await axios.post("/api/users/login/", {
          username: this.username,
          password: this.password,
        });

        const token = response.data.key;
        if (token) {
          localStorage.setItem("userToken", token);
          this.$store.dispatch("updateCurrentUser", {
            user: response.data.user_id,
            token: token,
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

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
  padding: 5px;
  position: relative;
}
</style>
