<template>
  <teleport to="body">
    <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ title }}</h3>
          <button class="btn btn-secondary btn-sm" @click="$emit('close')">X</button>
        </div>
        <div class="modal-body"><slot /></div>
        <div v-if="$slots.footer" class="modal-footer"><slot name="footer" /></div>
      </div>
    </div>
  </teleport>
</template>

<script setup>
defineProps({ show: Boolean, title: String })
defineEmits(['close'])
</script>
