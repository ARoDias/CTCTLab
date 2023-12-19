<!-- ModalComponent.vue -->

<!-- The template section defines the HTML structure of the modal component -->
<template>
  <div class="modal">
    <!-- iframe element to embed content, :src binds it to the iframeUrl prop -->
    <iframe ref="iframeElement" :src="iframeUrl"></iframe>
    <!-- Close button emits a 'close' event to the parent component when clicked -->
    <button class="close-button" @click="$emit('close')">Fechar</button>
  </div>
</template>

<!-- The script section contains the Vue.js logic for this component -->
<script>
export default {
  // Define props to receive iframeUrl from the parent component
  props: ['iframeUrl'],
  
  // Code to run when the component is mounted
  mounted() {
    // Add an event listener for the 'message' event
    window.addEventListener('message', this.receiveMessage, false);
  },
  
  // Code to run before the component is unmounted
  beforeUnmount() {
    // Remove the previously added event listener
    window.removeEventListener('message', this.receiveMessage);
  },

  // Define methods used within this component
  methods: {
    receiveMessage(event) {
      // Check if the message is coming from the expected origin
      if (event.origin !== "http://127.0.0.1:8000") {
        return;
      }
      
      // Handle the message and log it to the console
      const data = event.data;
      console.log("Received data:", data);
    }
  }
};
</script>

<!-- Scoped styles specifically for this component -->
<style scoped>
.close-button {
  position: absolute;
  top: 10px;
  right: 15px;
  font-size: 30px;
  cursor: pointer;
}
</style>
