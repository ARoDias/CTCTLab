// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// Import the store
import { useUserStore } from '@/stores/counter'

// ... dentro de um componente Vue ou composição API setup
const store = useUserStore()

// Lazy load components for better performance
const HomePage = require('../views/HomeView.vue')
const CourseProgram = require('../components/CourseProgram.vue')
const NewsCard = require('../components/NewsCard.vue')
const PrivacyPolicy = () => import('../components/PrivacyPolicy.vue')
const LoginModal = () => import('../components/LoginModal.vue')
const RegisterModal = () => import('../components/RegisterModal.vue')
const NotFound = () => import('../components/NotFound.vue')
const WeekComponent = () => import('../components/WeekComponent.vue')
const TPClassesComponent = () => import('../components/TPClassesComponent.vue')
const QuestionsComponent = () => import('../components/QuestionsComponent.vue')
const ResultComponent = () => import('../components/ResultComponent.vue')

// Define routes
const routes = [
  // Home page accessible only if authenticated
  { path: '', component: HomePage, meta: { requiresAuth: false } },
  { path: '/course', component: CourseProgram },
  { path: '/news', component: NewsCard },
  { path: '/privacy', component: PrivacyPolicy },
  { path: '/login', component: LoginModal },
  { path: '/register', component: RegisterModal },
  // WeekComponent and  TPClassesComponent accessible only if authenticated
  { path: '/week/:weekNumber', component: WeekComponent, meta: { requiresAuth: true } },
  { path: '/tp-classes', component: TPClassesComponent, meta: { requiresAuth: true } },
  { path: '/questions', component: QuestionsComponent, meta: { requiresAuth: true } },
  { path: '/result', component: ResultComponent, meta: { requiresAuth: true } },
  // Handle undefined routes
  { path: '/:catchAll(.*)', component: NotFound }
]

// Create and configure the router
const router = createRouter({
  history: createWebHistory(),
  routes
})

// Middleware: Navigation Guard
router.beforeEach((to, from, next) => {
  // Using optional chaining to avoid 'undefined' errors
  const isAuthenticated = store.getters.isLoggedIn
  // Redirect to login page if route requires authentication and user is not authenticated
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  }
  // Redirect authenticated users trying to access login or register back to home
  else if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
