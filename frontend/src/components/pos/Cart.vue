<template>
  <div class="cart-container card">
    <div class="cart-header">
      <h3>Keranjang</h3>
      <span class="cart-count">{{ cart.totalItems }} item</span>
    </div>

    <div class="cart-items" v-if="!cart.isEmpty">
      <CartItem
        v-for="item in cart.items"
        :key="item.product_id"
        :item="item"
        @update-quantity="cart.updateQuantity(item.product_id, $event)"
        @remove="cart.removeItem(item.product_id)"
      />
    </div>
    <div v-else class="empty-state" style="flex:1;">
      <p>Keranjang kosong</p>
    </div>

    <div class="cart-footer" v-if="!cart.isEmpty">
      <div class="cart-total">
        <span>Total</span>
        <strong>{{ formatCurrency(cart.totalPrice) }}</strong>
      </div>
      <button class="btn btn-primary btn-lg" style="width: 100%;" @click="$emit('checkout')">
        Bayar
      </button>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '../../stores/cart'
import { formatCurrency } from '../../utils/formatters'
import CartItem from './CartItem.vue'

const cart = useCartStore()
defineEmits(['checkout'])
</script>

<style scoped>
.cart-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - var(--navbar-height) - 3rem);
  padding: 0;
}
.cart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--gray-200);
}
.cart-header h3 { font-size: 1rem; font-weight: 600; }
.cart-count { font-size: 0.8125rem; color: var(--gray-500); }
.cart-items { flex: 1; overflow-y: auto; padding: 0.75rem; }
.cart-footer {
  border-top: 1px solid var(--gray-200);
  padding: 1rem 1.25rem;
}
.cart-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  font-size: 1.125rem;
}
</style>
