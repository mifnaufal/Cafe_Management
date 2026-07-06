<template>
  <div class="form-group">
    <label v-if="label">{{ label }}</label>
    <input
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :class="['input', { 'input-error': error }]"
      @input="$emit('update:modelValue', $event.target.value)"
    />
    <p v-if="error" class="form-error">{{ error }}</p>
  </div>
</template>

<script setup>
defineProps({ label: String, modelValue: [String, Number], type: { type: String, default: 'text' }, placeholder: String, error: String })
defineEmits(['update:modelValue'])
</script>
