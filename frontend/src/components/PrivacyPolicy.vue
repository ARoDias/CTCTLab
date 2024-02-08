<!-- components/PrivacyPolicy.vue -->
<template>
  <div class="modal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <!-- Modal header with title and close button -->
        <div class="modal-header">
          <h5 class="modal-title">Política de Privacidade / Privacy Policy</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            @click="closePrivacyPolicy"
            aria-label="Close"
          ></button>
        </div>
        <!-- Modal body with Portuguese and English sections -->
        <div class="modal-body">
          <!-- Portuguese privacy policy section -->
          <section>
            <h6>Português</h6>
            <p>
              Este pedido de consentimento destina-se a informá-lo claramente
              sobre como e porque a Faculdade de Ciências e Tecnologia da
              Universidade Nova de Lisboa (FCT NOVA) pretende utilizar os seus
              dados pessoais.
            </p>
            <p>
              A FCT NOVA planeia tratar os seus dados a fim de tirar
              considerações sobre processos de aprendizagem. Isto incluirá dados
              como os acessos à aplicação web, o tempo de resposta de cada
              atividade, informações pessoais excluindo o nome, e respostas a
              questionários.
            </p>
            <p>
              O seu consentimento é dado de livre vontade, é específico e
              informado, e reflete inequivocamente os seus desejos. O seu
              consentimento informado significa que você está a receber todas as
              informações relevantes sobre o tratamento dos seus dados, conforme
              descrito acima.
            </p>
            <p>
              Você tem a possibilidade de retirar o consentimento dado a
              qualquer momento, por exemplo, enviando uma mensagem de correio
              eletrónico para ctctbooster@gmail.com.
            </p>
          </section>
          <!-- Separator line -->
          <hr />
          <!-- English privacy policy section -->
          <section>
            <h6>English</h6>
            <p>
              This consent request is intended to clearly inform you about how
              and why the Faculty of Sciences and Technology of the New
              University of Lisbon (FCT NOVA) intends to use your personal data.
            </p>
            <p>
              FCT NOVA plans to process your data in order to draw conclusions
              about learning processes. This will include data such as web
              application accesses, response time for each activity, personal
              information excluding the name, and questionnaire responses.
            </p>
            <p>
              Your consent is given freely, is specific and informed, and
              unequivocally reflects your wishes. Your informed consent means
              you are receiving all the relevant information about the
              processing of your data, as described above.
            </p>
            <p>
              You have the possibility to withdraw the consent given at any
              time, for example, by sending an email message to
              ctctbooster@gmail.com.
            </p>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    // Method to emit an event to close the privacy policy modal
    closePrivacyPolicy() {
      this.$emit("closePolicy");
    },
  },
};
</script>

<style scoped>
/* Container for maximum width and central alignment */
.container {
  max-width: 600px;
  margin: auto;
  padding: 5px;
  position: relative;
}

/* Style for the modal backdrop */
.modal {
  display: block !important; /* Ensuring the modal displays */
  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent black background */
  color: #fff; /* White text for contrast */
}

/* Style for the modal dialog */
.modal-dialog {
  max-width: 100%; /* Utilize the maximum available width */
  margin: 1.75rem auto; /* Center and add vertical margin */
}

/* Style for the modal content */
.modal-content {
  background: var(--dark-blue); /* Using primary green color for background */
  color: var(--white); /* White text color */
  border-radius: var(--border-radius); /* Rounded corners */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3); /* Shadow for depth */
}

/* Style for the modal header */
.modal-header,
.modal-body {
  padding: 20px; /* Internal padding */
}

/* Style for the modal title */
.modal-title {
  margin: 0; /* Remove default margin */
  font-size: 1.25rem; /* Font size for title */
}

/* Style for the close button */
.btn-close {
  background: var(--white); /* White background for the close button */
  border-radius: 50%; /* Circular close button */
}

/* Style for the separator line */
hr {
  border: 0; /* Remove default border */
  height: 1px; /* Height of the line */
  background-image: linear-gradient(
    to right,
    rgba(255, 255, 255, 0),
    var(--white),
    rgba(255, 255, 255, 0)
  ); /* Gradient for the line */
}

/* Style for the subheadings */
h6 {
  font-size: 1rem; /* Font size for subheadings */
  margin-top: 20px; /* Space before subheading */
}

/* Style for each section in the modal body */
section {
  margin-bottom: 20px; /* Space after each section */
}
</style>
