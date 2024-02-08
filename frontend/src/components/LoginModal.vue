<template>
  <!-- Utiliza o componente modal genérico -->
  <ModalComponent
    :isVisible="showModal"
    @update:isVisible="handleVisibilityChange"
  >
    <template #header>
      <!-- Conteúdo personalizado para o cabeçalho do modal -->
      <h5 class="modal-title">LOGIN</h5>
    </template>

    <template #default>
      <!-- Corpo principal do modal, contendo o formulário de login -->
      <form @submit.prevent="submitLogin">
        <div class="form-group">
          <label for="username"
            >USERNAME (Número de aluno) (Student number)</label
          >
          <input
            type="text"
            id="username"
            v-model="username"
            autocomplete="username"
          />
        </div>
        <div class="form-group">
          <label for="password">SENHA (Password)</label>
          <input
            type="password"
            id="password"
            v-model="password"
            autocomplete="current-password"
          />
        </div>
        <div class="submit-button">
          <button class="btn btn-primary" type="submit">LOGIN</button>
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
import apiClient from "@/axiosConfig.js";
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
        const loginResponse = await apiClient.post("/api/users/login/", {
          username: this.username,
          password: this.password,
        });

        const { key: token } = loginResponse.data;
        if (token) {
          this.$store.dispatch("updateAuthToken", token);

          const userData = {
            id: loginResponse.data.user_id,
            username: this.username,
            is_student: loginResponse.data.user_type === "student",
            is_teacher: loginResponse.data.user_type !== "student",
            studentNumber:
              loginResponse.data.user_type === "student" ? this.username : null,
          };

          await this.$store.dispatch("updateCurrentUser", userData);
          await this.$store.dispatch("fetchAndSetUserProfile");

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
