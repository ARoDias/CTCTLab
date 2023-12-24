<template>
  <div class="modal-overlay" v-show="isVisible" @click.self="closeModal">
    <div class="modal-content" @click.stop>
      <header class="modal-header">
        <slot name="header"></slot>
        <button class="close-button" @click="closeModal">&times;</button>
      </header>

      <main class="modal-body">
        <slot></slot>
      </main>

      <footer class="modal-footer">
        <slot name="footer"></slot>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  props: ["isVisible"],
  emits: ["update:isVisible"],
  methods: {
    closeModal() {
      this.$emit("update:isVisible", false);
    },
  },
};
</script>

<style scoped>
.modal-body {
  padding: 10px;
  background-color: white;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.6);
  z-index: 1000;
  overflow-y: auto;
}

.modal-content {
  background: var(--white);
  border-radius: var(--border-radius);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  width: auto;
  max-width: 600px;
  margin: 20px;
  max-height: 90vh;
  overflow-y: auto;
  border: 1px solid var(--primary-blue);
}

.modal-header {
  background: var(--primary-blue);
  color: var(--white);
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 101;
  border-top-right-radius: var(--border-radius);
  border-top-left-radius: var(--border-radius);
}

.close-button {
  background: none;
  border: none;
  color: var(--white);
  font-size: 1.5em;
  cursor: pointer;
}
</style>
