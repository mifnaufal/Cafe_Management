<template>
  <header class="navbar">
    <div class="navbar-left">
      <h2 class="page-title">{{ pageTitle }}</h2>
    </div>
    <div class="navbar-right">
      <span class="user-role badge" :class="auth.isAdmin ? 'badge-success' : 'badge-gray'">
        {{ auth.userRole }}
      </span>
      <span class="user-name">{{ auth.userName }}</span>
      <button class="btn btn-secondary btn-sm" @click="handleLogout">Logout</button>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const pageTitles = {
  '/dashboard': 'Dashboard',
  '/pos': 'POS (Point of Sale)',
  '/products': 'Produk',
  '/categories': 'Kategori',
  '/transactions': 'Riwayat Transaksi',
}

const pageTitle = computed(() => {
  if (route.path.startsWith('/transactions/') && route.params.id) return 'Detail Transaksi'
  return pageTitles[route.path] || 'POS Lite'
})

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: var(--sidebar-width);
  right: 0;
  height: var(--navbar-height);
  background: #fff;
  border-bottom: 1px solid var(--gray-200);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  z-index: 50;
}
.page-title {
  font-size: 1.25rem;
  font-weight: 600;
}
.navbar-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.user-name {
  font-size: 0.875rem;
  color: var(--gray-700);
}
</style>
