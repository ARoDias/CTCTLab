<template>
  <ModalComponent :isVisible="show" @update:isVisible="close">
    <template #header>
      <!-- Aqui você pode customizar o cabeçalho do modal -->
      <h5 class="modal-title">Questionário</h5>
    </template>

    <template #default>
      <!-- Conteúdo do modal -->
      <div class="modal-body-custom">
        <slot></slot>
      </div>
    </template>

    <template #footer>
      <!-- Aqui você pode adicionar conteúdo ao rodapé se necessário -->
    </template>
  </ModalComponent>
</template>

<script>
import ModalComponent from "@/components/ModalComponent.vue";

export default {
  components: {
    ModalComponent,
  },
  props: ["show"],
  emits: ["close"],
  methods: {
    close() {
      this.$emit("close");
    },
  },
};
</script>

<style scoped></style>
