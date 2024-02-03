<!-- components/PrivacyPolicy.vue -->
<template>
  <div class="modal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Termos da Política de Privacidade</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            @click="closePrivacyPolicy"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <p>
            Este pedido de consentimento destina-se a informá-lo claramente
            sobre como e porque a Faculdade de Ciências e Tecnologia da
            Universidade Nova de Lisboa (FCT NOVA) pretende utilizar os seus
            dados pessoais.
          </p>
          <p>
            A FCT NOVA planeia tratar os seus dados a fim de tirar considerações
            sobre processos de aprendizagem. Isto incluirá dados como os acessos
            à aplicação web, o tempo de resposta de cada atividade, informações
            pessoais excluindo o nome, e respostas a questionários.
          </p>
          <p>
            O seu consentimento é dado de livre vontade, é específico e
            informado, e reflete inequivocamente os seus desejos. O seu
            consentimento informado significa que você está a receber todas as
            informações relevantes sobre o tratamento dos seus dados, conforme
            descrito acima.
          </p>
          <p>
            Você tem a possibilidade de retirar o consentimento dado a qualquer
            momento, por exemplo, enviando uma mensagem de correio eletrónico
            para ctctbooster@gmail.com.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    closePrivacyPolicy() {
      this.$emit("closePolicy");
    },
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

.modal {
  display: block !important;
  background-color: rgba(0, 0, 0, 0.7);
  color: #446ebc;
}
</style>
