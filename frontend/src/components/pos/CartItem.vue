<template>
  <div class="cart-item">
    <div class="item-info">
      <div class="item-name">{{ item.product_name }}</div>
      <div class="item-price">{{ formatCurrency(item.price_at_time) }}</div>
    </div>
    <div class="item-actions">
      <button class="qty-btn" @click="$emit('updateQuantity', item.quantity - 1)">-</button>
      <span class="qty-value">{{ item.quantity }}</span>
      <button class="qty-btn" @click="$emit('updateQuantity', item.quantity + 1)">+</button>
      <button class="remove-btn" @click="$emit('remove')">X</button>
    </div>
    <div class="item-subtotal">{{ formatCurrency(item.subtotal) }}</div>
  </div>
</template>

<script setup>
import { formatCurrency } from '../../utils/formatters'
defineProps({ item: Object })
defineEmits(['updateQuantity', 'remove'])
</script>

<style scoped>
.cart-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0.75rem;
  border-bottom: 1px solid var(--gray-100);
}
.item-info { display: flex; justify-content: space-between; }
.item-name { font-weight: 500; font-size: 0.875rem; }
.item-price { color: var(--gray-500); font-size: 0.8125rem; }
.item-actions { display: flex; align-items: center; gap: 0.5rem; }
.qty-btn {
  width: 28px; height: 28px;
  border: 1px solid var(--gray-300);
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
}
.qty-value { font-weight: 600; min-width: 20px; text-align: center; }
.remove-btn {
  margin-left: auto;
  border: none; background: none;
  color: var(--danger); cursor: pointer;
  font-size: 0.8125rem;
}
.item-subtotal { text-align: right; font-weight: 600; font-size: 0.875rem; }
</style>
