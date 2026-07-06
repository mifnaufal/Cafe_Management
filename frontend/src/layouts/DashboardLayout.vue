<template>
  <div class="dashboard-layout">
    <AppSidebar />
    <div class="main-area">
      <AppNavbar />
      <main class="main-content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import AppSidebar from '../components/layout/AppSidebar.vue'
import AppNavbar from '../components/layout/AppNavbar.vue'
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  min-height: 100vh;
}
.main-area {
  flex: 1;
  margin-left: var(--sidebar-width);
  display: flex;
  flex-direction: column;
}
.main-content {
  flex: 1;
  padding: 1.5rem;
  margin-top: var(--navbar-height);
}
</style>
