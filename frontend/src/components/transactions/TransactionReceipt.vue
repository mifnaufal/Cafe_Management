<template>
  <div class="receipt">
    <div class="receipt-header">
      <strong>POS Lite</strong>
      <p style="font-size: 0.75rem; color: var(--gray-500);">Jl. Example No. 123</p>
    </div>
    <div class="receipt-divider" />
    <div class="receipt-info">
      <p>#{{ transaction.transaction_number }}</p>
      <p style="font-size: 0.75rem;">{{ formatDate(transaction.created_at) }}</p>
      <p style="font-size: 0.75rem;">Kasir: {{ transaction.cashier?.full_name || '-' }}</p>
    </div>
    <div class="receipt-divider" />
    <div class="receipt-items">
      <div class="receipt-item" v-for="item in transaction.items" :key="item.id">
        <div class="item-line">
          <span class="item-name-receipt">{{ item.product_name }}</span>
          <span class="item-amount">{{ formatCurrency(item.subtotal) }}</span>
        </div>
        <div class="item-qty">{{ item.quantity }} x {{ formatCurrency(item.price_at_time) }}</div>
      </div>
    </div>
    <div class="receipt-divider" />
    <div class="receipt-total">
      <span>Total</span>
      <strong>{{ formatCurrency(transaction.total_amount) }}</strong>
    </div>
    <div class="receipt-divider" />
    <div class="receipt-footer">
      <p>Terima kasih!</p>
      <p style="font-size: 0.75rem;">Barang yang sudah dibeli tidak dapat dikembalikan</p>
    </div>
  </div>
</template>

<script setup>
import { formatCurrency, formatDate } from '../../utils/formatters'
defineProps({ transaction: { type: Object, required: true } })
</script>

<style scoped>
.receipt {
  background: #fff;
  font-size: 0.8125rem;
  text-align: left;
}
.receipt-header { text-align: center; margin-bottom: 0.5rem; }
.receipt-divider { border-top: 1px dashed var(--gray-300); margin: 0.5rem 0; }
.receipt-info p { margin-bottom: 0.125rem; }
.receipt-item { margin-bottom: 0.5rem; }
.item-line { display: flex; justify-content: space-between; }
.item-name-receipt { font-weight: 500; }
.item-amount { }
.item-qty { font-size: 0.75rem; color: var(--gray-500); }
.receipt-total {
  display: flex; justify-content: space-between;
  font-size: 1rem; font-weight: 700;
}
.receipt-footer { text-align: center; color: var(--gray-500); font-size: 0.75rem; }
.receipt-footer p { margin-bottom: 0.125rem; }
</style>
