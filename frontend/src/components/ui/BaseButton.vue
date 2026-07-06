<template>
  <button :class="['btn', `btn-${variant}`, size === 'sm' ? 'btn-sm' : size === 'lg' ? 'btn-lg' : '']" :disabled="disabled">
    <slot />
  </button>
</template>

<script setup>
defineProps({ variant: { type: String, default: 'primary' }, size: { type: String, default: 'md' }, disabled: Boolean })
</script>
