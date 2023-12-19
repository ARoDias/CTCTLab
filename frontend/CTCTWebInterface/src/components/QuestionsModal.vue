<template>
  <div v-if="show" class="modal-overlay" @click.self="close">
    <div class="modal">
      <div class="modal-header">
        <button class="close-button" @click="close">Fechar</button>
      </div>
      <div class="modal-body">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['show'],
  emits: ['close'],
  methods: {
    close() {
      this.$emit('close');
    },
  },
};
</script>


