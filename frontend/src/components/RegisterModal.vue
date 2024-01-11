<!-- components/RegisterModal.vue -->
<template>
  <!-- Utilize ModalComponent para envolver o formulário de registro -->
  <ModalComponent
    :isVisible="showModal"
    @update:isVisible="handleVisibilityChange"
  >
    <template #header>
      <h5 class="modal-title">Registo do Aluno</h5>
    </template>

    <template #default>
      <form method="POST" @submit.prevent="submitRegister" class="form-group">
        <div class="field-group">
          <label for="username">Número de Aluno:</label>
          <input
            type="text"
            id="username"
            v-model="username"
            required
            autocomplete="username"
          />

          <label for="email">Email:</label>
          <input
            type="email"
            id="email"
            v-model="email"
            required
            autocomplete="email"
          />
        </div>

        <div class="field-group">
          <div class="formfield">
            <label for="password1">Senha:</label>
            <input
              type="password"
              id="password1"
              v-model="password1"
              pattern=".{8,}"
              title="Deve conter pelo menos 8 caracteres"
              required
              autocomplete="asdasdasd"
            />
          </div>
          <div class="formfield">
            <label for="password2">Confirmação da senha:</label>
            <input
              type="password"
              id="password2"
              v-model="password2"
              pattern=".{8,}"
              title="Deve conter pelo menos 8 caracteres"
              required
              autocomplete="asdasdasd"
            />
          </div>
        </div>
        <hr />
        <div class="row">
          <div class="col">
            <input
              type="text"
              class="form-control"
              placeholder="Primeiro Nome"
              aria-label="First name"
              id="first_name"
              v-model="first_name"
              required
              autocomplete="given-name"
            />
          </div>
          <div class="col">
            <input
              type="text"
              class="form-control"
              placeholder="Apelido"
              aria-label="Last name"
              id="last_name"
              v-model="last_name"
              required
              autocomplete="family-name"
            />
          </div>
        </div>

        <div class="field-group">
          <div class="formfield">
            <label for="course">Curso: </label>
            <select id="course" v-model="course" required>
              <option disabled value="">Escolhe um curso</option>
              <option
                v-for="course in courses"
                :key="course.id"
                :value="course.name"
              >
                {{ course.name }}
              </option>
            </select>
          </div>

          <div class="field-group">
            <div class="formfield">
              <label for="age">Idade:</label>
              <input type="number" id="age" v-model="age" required />
            </div>
            <label for="gender">Género: </label><br />
            <input
              type="radio"
              id="feminino"
              name="gender"
              value="F"
              v-model="gender"
            />
            <label for="feminino">Feminino</label><br />
            <input
              type="radio"
              id="masculino"
              name="gender"
              value="M"
              v-model="gender"
            />
            <label for="masculino">Masculino</label><br />
            <input
              type="radio"
              id="outro"
              name="gender"
              value="O"
              v-model="gender"
            />
            <label for="outro">Outro / Prefiro não dizer</label>
          </div>
        </div>

        <div text-align="left" class="consent-field">
          <label for="data_consent">
            <input
              type="checkbox"
              id="data_consent"
              v-model="data_consent"
              required
            />
            Concordo com a
            <a href="#" @click.prevent="openPrivacyPolicy">recolha de dados</a>
          </label>
        </div>
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
        <div class="submit-button">
          <button class="btn btn-primary" type="submit">Registar</button>
        </div>
      </form>

      <!-- Política de Privacidade Modal -->
      <PrivacyPolicy
        v-if="showPrivacyPolicy"
        @closePolicy="handleClosePolicy"
      />
    </template>

    <template #footer>
      <!-- Conteúdo do rodapé do modal, se necessário -->
    </template>
  </ModalComponent>
</template>

<script>
// Importações necessárias e a lógica do componente permanecem as mesmas
import axios from "axios";
import { getCookie, setCookie } from "./utilities.js";
import PrivacyPolicy from "./PrivacyPolicy.vue";
import ModalComponent from "@/components/ModalComponent.vue"; // Certifique-se de que o caminho está correto

export default {
  components: {
    ModalComponent,
    PrivacyPolicy,
  },
  data() {
    return {
      username: "",
      password: "",
      password1: "", // Store the entered password
      password2: "", // Store the entered password
      email: "",
      first_name: "",
      last_name: "",
      course: null,
      age: 18,
      gender: "",
      data_consent: false,
      courses: [],
      showPrivacyPolicy: false,
      errorMessage: null,
      weeknumber: 1,
      showModal: true, // Show or hide the modal
    };
  },
  methods: {
    closeModal() {
      this.showModal = false; // Set showModal to false to hide it
      document.title = "CTCTLab";
      this.$emit("closeModal"); // Emit event to parent component
    },
    handleVisibilityChange(value) {
      this.showModal = value;
    },
    openPrivacyPolicy() {
      this.showPrivacyPolicy = true;
    },
    handleClosePolicy() {
      this.showPrivacyPolicy = false;
    },
    async fetchCourses() {
      try {
        const response = await axios.get("/api/users/courses/");
        this.courses = response.data;
      } catch (error) {
        console.error("Erro ao buscar cursos:", error);
      }
    },

    async submitRegister() {
      this.errorMessage = null;
      if (this.password1 !== this.password2) {
        this.errorMessage = "As senhas não coincidem.";
        return;
      }

      const payload = {
        username: this.username,
        password: this.password1,
        email: this.email,
        first_name: this.first_name,
        last_name: this.last_name,
        course: this.course,
        age: this.age,
        gender: this.gender,
        data_consent: this.data_consent,
      };

      try {
        const response = await axios.post("/api/users/register/", payload, {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
          },
        });

        if (response.status === 200 || response.status === 201) {
          setCookie("user_registered", "true", 1);
          setCookie("user_type", "student", 1);
          setCookie("user_id", response.data.user_id, 1);

          // Assuming the token is sent in the response for successful registration
          this.$store.dispatch("updateAuthToken", response.data.token);
          this.$store.dispatch("updateCurrentUser", {
            user: response.data.user_id,
          });

          this.$router.push("/");
          this.closeModal();
        }
      } catch (error) {
        this.errorMessage =
          error.response?.data?.detail ||
          "Houve um problema ao submeter o formulário.";
        console.error("Registration Error:", error);
      }
    },
  },
  created() {
    this.fetchCourses();
    document.title = "Registo";
  },
};
</script>
