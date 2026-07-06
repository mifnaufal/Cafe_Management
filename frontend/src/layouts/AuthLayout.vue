<template>
  <div class="auth-layout">
    <div class="auth-container">
      <div class="card auth-card">
        <slot />
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #D4F1D4;
  padding: 1rem;
}
.auth-container {
  width: 100%;
  max-width: 420px;
}
.auth-card {
  background: #fff;
  border: none;
  border-radius: 24px;
  padding: 2.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}
</style>
