// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia' // Import Pinia for state management
import 'bootstrap/dist/css/bootstrap.min.css'
import axios from 'axios'
import './assets/base.css'
import './assets/main.css'
// Configure Axios if necessary
axios.defaults.baseURL = 'http://127.0.0.1:8000'

// Create the Vue app
const app = createApp(App)

// Use Pinia for state management
const pinia = createPinia()
app.use(pinia)

// Use Vue Router
app.use(router)

// Mount the app
app.mount('#app')
