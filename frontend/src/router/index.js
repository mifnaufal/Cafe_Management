import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/LoginView.vue'),
    meta: { layout: 'auth' },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/auth/RegisterView.vue'),
    meta: { layout: 'auth' },
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/dashboard/DashboardView.vue'),
    meta: { layout: 'dashboard' },
  },
  {
    path: '/products',
    name: 'Products',
    component: () => import('../views/dashboard/ProductsView.vue'),
    meta: { layout: 'dashboard' },
  },
  {
    path: '/categories',
    name: 'Categories',
    component: () => import('../views/dashboard/CategoriesView.vue'),
    meta: { layout: 'dashboard' },
  },
  {
    path: '/pos',
    name: 'POS',
    component: () => import('../views/dashboard/POSView.vue'),
    meta: { layout: 'dashboard' },
  },
  {
    path: '/transactions',
    name: 'TransactionHistory',
    component: () => import('../views/dashboard/TransactionHistoryView.vue'),
    meta: { layout: 'dashboard' },
  },
  {
    path: '/transactions/:id',
    name: 'TransactionDetail',
    component: () => import('../views/dashboard/TransactionDetailView.vue'),
    meta: { layout: 'dashboard' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  const requiresAuth = to.meta.layout === 'dashboard'
  const isAuthPage = to.meta.layout === 'auth'

  if (requiresAuth && !auth.isAuthenticated) {
    next('/login')
  } else if (isAuthPage && auth.isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
