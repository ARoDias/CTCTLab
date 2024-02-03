// src/axiosConfig.js
import axios from "axios";
import store from "./store";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

const apiClient = axios.create({
  baseURL: "https://throbbing-river-82258.pktriot.net/",
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use(
  (config) => {
    // Exclude the Authorization header for login requests
    if (config.url !== "/api/users/login/") {
      const token = store.getters.getAuthToken;
      //console.log(token);
      if (token) {
        config.headers["Authorization"] = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  (response) => response, // this function handles successful responses
  async (error) => {
    const originalRequest = error.config;

    // Check if we received a 401 response, which means the token expired
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true; // mark it so we don't try to refresh the token repeatedly

      // Try to get a new token using the refresh token
      const refreshToken = localStorage.getItem("userRefreshToken"); // replace with actual refresh token key
      if (refreshToken) {
        try {
          const tokenResponse = await axios.post("/api/users/token/refresh/", {
            refresh: refreshToken,
          });
          const { access } = tokenResponse.data;

          // Update the token in the store and local storage
          store.dispatch("updateAuthToken", access);

          // Resend the original request with the new token
          originalRequest.headers["Authorization"] = "Bearer " + access;
          return apiClient(originalRequest);
        } catch (refreshError) {
          // Handle failed refresh here (e.g., redirect to login)
          return Promise.reject(refreshError);
        }
      }
    }

    // Return any error which is not due to authentication
    return Promise.reject(error);
  }
);

export default apiClient;
