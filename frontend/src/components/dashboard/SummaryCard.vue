<template>
  <div class="card summary-card">
    <p class="summary-title">{{ title }}</p>
    <p class="summary-amount">{{ formatCurrency(amount) }}</p>
    <p class="summary-subtitle" v-if="subtitle">{{ subtitle }}</p>
  </div>
</template>

<script setup>
import { formatCurrency } from '../../utils/formatters'
defineProps({ title: String, amount: Number, subtitle: String })
</script>

<style scoped>
.summary-card { padding: 1.25rem; }
.summary-title { font-size: 0.8125rem; color: var(--gray-500); margin-bottom: 0.25rem; }
.summary-amount { font-size: 1.5rem; font-weight: 700; color: var(--gray-900); }
.summary-subtitle { font-size: 0.75rem; color: var(--gray-400); margin-top: 0.25rem; }
</style>
