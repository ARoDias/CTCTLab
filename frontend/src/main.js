// frontend/src/main.js

// Import necessary modules
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import axios from "axios";
import store from "./store"; // Import Vuex store
import "bootstrap/dist/css/bootstrap.min.css";
import "./axiosConfig";

// Set the baseURL for axios
axios.defaults.baseURL = "https://throbbing-river-82258.pktriot.net";
//axios.defaults.baseURL ="https://78ec-2a01-14-8020-7e20-e9d2-9197-151a-7ef.ngrok-free.app";
//axios.defaults.baseURL = "http://127.0.0.1:8000/";
// Create the Vue app
const app = createApp(App);

// Use Vuex store
app.use(store);

// Use Vue Router
app.use(router);

// Attach axios instance as a global property
app.config.globalProperties.$axios = axios;

// Mount the app
app.mount("#app");
