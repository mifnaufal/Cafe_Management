<template>
  <aside class="sidebar">
    <div class="sidebar-brand">
      <div class="brand-icon">P</div>
      <span class="brand-text">POS Lite</span>
    </div>
    <nav class="sidebar-nav">
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="nav-item"
        :class="{ active: isActive(item.path) }"
      >
        <span class="nav-icon" v-html="item.icon" />
        <span class="nav-label">{{ item.label }}</span>
      </router-link>
    </nav>
    <div class="sidebar-footer">
      <span class="version">v1.0.0</span>
    </div>
  </aside>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const route = useRoute()
const auth = useAuthStore()

const menuItems = [
  { path: '/dashboard', label: 'Dashboard', icon: '&#9632;' },
  { path: '/pos', label: 'POS', icon: '&#9733;' },
  { path: '/products', label: 'Produk', icon: '&#9679;' },
  { path: '/categories', label: 'Kategori', icon: '&#9641;' },
  { path: '/transactions', label: 'Transaksi', icon: '&#9776;' },
]

function isActive(path) {
  if (path === '/dashboard') return route.path === '/dashboard'
  return route.path.startsWith(path)
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: var(--sidebar-width);
  height: 100vh;
  background: var(--gray-900);
  color: #fff;
  display: flex;
  flex-direction: column;
  z-index: 100;
}
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.brand-icon {
  width: 36px;
  height: 36px;
  background: var(--primary);
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.25rem;
}
.brand-text {
  font-size: 1.125rem;
  font-weight: 600;
}
.sidebar-nav {
  flex: 1;
  padding: 1rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: var(--radius);
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 0.875rem;
  transition: all 0.15s;
}
.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  text-decoration: none;
}
.nav-item.active {
  background: var(--primary);
  color: #fff;
}
.nav-icon {
  font-size: 1rem;
  width: 20px;
  text-align: center;
}
.sidebar-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}
.version {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.4);
}
</style>
