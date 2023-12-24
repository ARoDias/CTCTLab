<template>
  <ModalComponent :isVisible="show" @update:isVisible="close">
    <template #header>
      <h5 class="modal-title">Questionário</h5>
    </template>

    <template #default>
      <div class="modal-body-custom">
        <slot></slot>
      </div>
    </template>

    <template #footer>
      <!-- Rodapé, se necessário -->
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
