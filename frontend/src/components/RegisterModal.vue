<!-- components/RegisterModal.vue -->
<template>
  <!-- Utilize ModalComponent para envolver o formulário de registro -->
  <ModalComponent
    :isVisible="showModal"
    @update:isVisible="handleVisibilityChange"
  >
    <template #header>
      <h5 class="modal-title">
        FORMULÁRIO DE REGISTO<br />
        Registration Form
      </h5>
    </template>

    <template #default>
      <form method="POST" @submit.prevent="submitRegister" class="form-group">
        <div class="field-group">
          <label for="username"
            >NÚMERO DE ALUNO <br />
            Student Number</label
          >
          <input
            type="text"
            id="username"
            v-model="username"
            required
            autocomplete="username"
          />

          <label for="email">EMAIL</label>
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
            <label for="password1">SENHA <br />Password</label>
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
            <label for="password2"
              >CONFIRMAÇÃO DE SENHA <br />Password Confirmation</label
            >
            <input
              type="password"
              id="password2"
              v-model="password2"
              pattern=".{8,}"
              title="Deve conter pelo menos 8 caracteres - Should contain at least 6 chars!"
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
              placeholder="Nome"
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
            <label for="course">CURSO <br />Course</label>
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
              <label for="age"
                >IDADE<br />
                Age</label
              >
              <input type="number" id="age" v-model="age" required />
            </div>
            <label for="gender">GÉNERO <br />Gender </label><br />
            <input
              type="radio"
              id="feminino"
              name="gender"
              value="F"
              v-model="gender"
            />
            <label for="feminino"> Feminino (Female) </label><br />
            <input
              type="radio"
              id="masculino"
              name="gender"
              value="M"
              v-model="gender"
            />
            <label for="masculino"> Masculino (Male) </label><br />
            <input
              type="radio"
              id="outro"
              name="gender"
              value="O"
              v-model="gender"
            />
            <label for="outro"> Prefiro não dizer (I rather not say)</label>
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
            Eu concordo com a
            <a href="#" @click.prevent="openPrivacyPolicy"
              >política de privacidade.</a
            ><br />
            (I agree with the
            <a href="#" @click.prevent="openPrivacyPolicy">Privacy Policy)</a>
          </label>
        </div>
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
        <div class="submit-button">
          <button class="btn btn-primary" type="submit">
            REGISTAR / Register
          </button>
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
import apiClient from "@/axiosConfig";
//import { getCookie, setCookie } from "./utilities.js";
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
        // Using apiClient instead of axios directly for API requests
        const response = await apiClient.get("api/users/courses/");
        this.courses = response.data;
      } catch (error) {
        console.error("Error fetching courses:", error);
        this.errorMessage = "Erro a carregar cursos. Tente mais tarde.";
      }
    },

    async submitRegister() {
      this.errorMessage = null;
      if (this.password1 !== this.password2) {
        this.errorMessage =
          "As passwords não são iguais. Passwords don't match.";
        return;
      }
      if (!/^\d+$/.test(this.username)) {
        this.errorMessage =
          "Registo apenas para alunos: username deverá ser o número de aluno.";
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
        // Use apiClient instead of axios directly
        const response = await apiClient.post("api/users/register/", payload);

        // Assuming the backend sends back a success response
        if (response.status === 201) {
          // Handle success, for example, showing a success message
          // and/or redirecting the user
          alert(
            "A coordenação de CTCT agradece o seu registo. Por favor, proceda à ativação da conta através do link que recebeu no e-mail antes de realizar o login."
          );
          alert(
            "The CTCT coordination thanks you for registering. Please activate your account using the link you received in the email before logging in."
          );
          // Reset form or redirect user here
          this.closeModal(); // Assuming you have a method to close the modal
        }
      } catch (error) {
        // If an error occurs, handle it, for example by setting an error message
        this.errorMessage =
          error.response?.data?.detail ||
          "Houve um problema a submeter o formulário de registo.";
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
