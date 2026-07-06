<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h3>Konfirmasi Pembayaran</h3>
        <button class="btn btn-secondary btn-sm" @click="$emit('close')">X</button>
      </div>
      <div class="modal-body">
        <table class="table" style="margin-bottom: 1rem;">
          <thead>
            <tr>
              <th>Item</th>
              <th class="text-right">Qty</th>
              <th class="text-right">Subtotal</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in cart.items" :key="item.product_id">
              <td>{{ item.product_name }}</td>
              <td class="text-right">{{ item.quantity }}</td>
              <td class="text-right">{{ formatCurrency(item.subtotal) }}</td>
            </tr>
          </tbody>
        </table>
        <div class="flex justify-between" style="font-size: 1.25rem; font-weight: 700; padding: 0.75rem 0;">
          <span>Total</span>
          <span>{{ formatCurrency(cart.totalPrice) }}</span>
        </div>
        <div class="form-group">
          <label>Metode Pembayaran</label>
          <select v-model="paymentMethod" class="input">
            <option value="cash">Tunai</option>
            <option value="card">Kartu</option>
            <option value="ewallet">E-Wallet</option>
          </select>
        </div>
        <div class="form-group">
          <label>Catatan (opsional)</label>
          <input v-model="notes" class="input" placeholder="Catatan untuk transaksi" />
        </div>
        <p v-if="error" class="form-error">{{ error }}</p>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="$emit('close')">Batal</button>
        <button class="btn btn-primary btn-lg" :disabled="processing" @click="handleCheckout">
          {{ processing ? 'Memproses...' : `Bayar ${formatCurrency(cart.totalPrice)}` }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCartStore } from '../../stores/cart'
import { createTransaction } from '../../api/transactions'
import { formatCurrency } from '../../utils/formatters'

const cart = useCartStore()
const emit = defineEmits(['close'])

const paymentMethod = ref('cash')
const notes = ref('')
const processing = ref(false)
const error = ref('')

async function handleCheckout() {
  processing.value = true
  error.value = ''
  try {
    await createTransaction({
      items: cart.items.map((i) => ({ product_id: i.product_id, quantity: i.quantity })),
      payment_method: paymentMethod.value,
      notes: notes.value || null,
    })
    cart.clear()
    alert('Transaksi berhasil!')
    emit('close')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Transaksi gagal'
  } finally {
    processing.value = false
  }
}
</script>
