// CTCTLab\frontend\src\router.js
import store from "./store";
import { createRouter, createWebHistory } from "vue-router";

// Lazy load components for better performance
const HomePage = () => import("./components/HomePage.vue");
const CourseProgram = () => import("./components/CourseProgram.vue");
const NewsCard = () => import("./components/NewsCard.vue");
const PrivacyPolicy = () => import("./components/PrivacyPolicy.vue");
const LoginModal = () => import("./components/LoginModal.vue");
const RegisterModal = () => import("./components/RegisterModal.vue");
const NotFound = () => import("./components/NotFound.vue");
const WeekComponent = () => import("./components/WeekComponent.vue");
const TPClassesComponent = () => import("./components/TPClassesComponent.vue");
const TeacherDashboard = () => import("./components/TeacherDashboard.vue");
const QuestionsComponent = () => import("./components/QuestionsComponent.vue");
//const ResultComponent = () => import("./components/ResultComponent.vue");
// Define routes
const routes = [
  // Home page accessible only if authenticated
  { path: "", component: HomePage, meta: { requiresAuth: false } },
  { path: "/course", component: CourseProgram },
  { path: "/news", component: NewsCard },
  { path: "/privacy", component: PrivacyPolicy },
  { path: "/login", component: LoginModal },
  { path: "/register", component: RegisterModal },
  // WeekComponent and  TPClassesComponent accessible only if authenticated
  {
    path: "/week/:weekNumber",
    component: WeekComponent,
    meta: { requiresAuth: true },
  },
  {
    path: "/tp-classes",
    component: TPClassesComponent,
    meta: { requiresAuth: true },
  },
  {
    path: "/quizzDashboard",
    component: TeacherDashboard,
    meta: { requiresAuth: true },
  },
  {
    path: "/questions",
    component: QuestionsComponent,
    meta: { requiresAuth: true },
  },

  // Handle undefined routes
  { path: "/:catchAll(.*)", component: NotFound },
];

// Create and configure the router
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Middleware: Navigation Guard
router.beforeEach((to, from, next) => {
  // Using optional chaining to avoid 'undefined' errors
  const isAuthenticated = store.getters.isLoggedIn;
  // Redirect to login page if route requires authentication and user is not authenticated
  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/login");
  }
  // Redirect authenticated users trying to access login or register back to home
  else if (
    (to.path === "/login" || to.path === "/register") &&
    isAuthenticated
  ) {
    next("/");
  } else {
    next();
  }
});

export default router;
