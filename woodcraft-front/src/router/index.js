import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import LoginView from '../views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresAuth: false }
    },
    {
      path: '/kanban',
      name: 'kanban',
      component: () => import('../views/KanbanView.vue'),
      meta: { requiresAuth: true, requireAdmin: true }
    },
    {
      path: '/order/:id',
      name: 'order-detail',
      component: () => import('../views/OrderView.vue'),
      meta: { requiresAuth: true, requireAdmin: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/WorkerDashView.vue'),
      meta: { requiresAuth: true, requireWorker: true }
    },
    {
      path: '/products',
      name: 'products',
      component: () => import('../views/ProductsView.vue'),
      meta: { requiresAuth: true, requireAdmin: true }
    },
    {
      path: '/workers',
      name: 'workers',
      component: () => import('../views/WorkersView.vue'),
      meta: { requiresAuth: true, requireAdmin: true }
    },
    {
      path: '/templates',
      name: 'templates',
      component: () => import('../views/TemplatesView.vue'),
      meta: { requiresAuth: true, requireAdmin: true }
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('../views/SettingsView.vue'),
      meta: { requiresAuth: true, requireAdmin: true }
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: () => import('../views/AnalyticsView.vue'),
      meta: { requiresAuth: true, requireAdmin: true }
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: to => {
        return { path: '/login' }
      }
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Ensure user is fetched if we have token but no user object
  if (authStore.token && !authStore.user) {
    await authStore.fetchUser()
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' })
  } else if (to.name === 'login' && authStore.isAuthenticated) {
    if (authStore.isAdmin) next({ name: 'kanban' })
    else next({ name: 'dashboard' })
  } else if (to.meta.requireAdmin && !authStore.isAdmin) {
    next({ name: 'dashboard' }) // workers trying to access admin
  } else if (to.meta.requireWorker && authStore.isAdmin) {
    next({ name: 'kanban' }) // admin trying to access worker dash
  } else {
    next()
  }
})

export default router
