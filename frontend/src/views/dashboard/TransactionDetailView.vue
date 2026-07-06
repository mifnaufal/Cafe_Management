<template>
  <div>
    <router-link to="/transactions" class="btn btn-secondary btn-sm" style="margin-bottom: 1rem;">
      &larr; Kembali
    </router-link>

    <div v-if="loading" class="loading"><div class="spinner" /></div>
    <div v-else-if="transaction">
      <div class="grid" style="grid-template-columns: 2fr 1fr; gap: 1.5rem;">
        <div class="card">
          <h3 style="margin-bottom: 1rem; font-size: 1.125rem;">Detail Transaksi</h3>
          <table class="table" style="margin-bottom: 1rem;">
            <tbody>
              <tr><td style="width: 140px; font-weight: 500;">No. Transaksi</td><td><strong>{{ transaction.transaction_number }}</strong></td></tr>
              <tr><td style="font-weight: 500;">Tanggal</td><td>{{ formatDate(transaction.created_at) }}</td></tr>
              <tr><td style="font-weight: 500;">Kasir</td><td>{{ transaction.cashier?.full_name || '-' }}</td></tr>
              <tr><td style="font-weight: 500;">Pembayaran</td><td><span class="badge badge-gray">{{ getPaymentMethodLabel(transaction.payment_method) }}</span></td></tr>
              <tr><td style="font-weight: 500;">Catatan</td><td>{{ transaction.notes || '-' }}</td></tr>
            </tbody>
          </table>

          <h4 style="margin-bottom: 0.75rem; font-size: 0.875rem;">Item</h4>
          <table class="table">
            <thead>
              <tr>
                <th>Produk</th>
                <th class="text-right">Harga</th>
                <th class="text-right">Qty</th>
                <th class="text-right">Subtotal</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in transaction.items" :key="item.id">
                <td>{{ item.product_name }}</td>
                <td class="text-right">{{ formatCurrency(item.price_at_time) }}</td>
                <td class="text-right">{{ item.quantity }}</td>
                <td class="text-right">{{ formatCurrency(item.subtotal) }}</td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="3" class="text-right" style="font-weight: 600;">Total</td>
                <td class="text-right" style="font-weight: 600;">{{ formatCurrency(transaction.total_amount) }}</td>
              </tr>
            </tfoot>
          </table>
        </div>

        <div class="card" style="text-align: center;">
          <h3 style="margin-bottom: 1rem; font-size: 1.125rem;">Struk</h3>
          <TransactionReceipt :transaction="transaction" />
        </div>
      </div>
    </div>
    <div v-else class="empty-state"><p>Transaksi tidak ditemukan</p></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getTransaction } from '../../api/transactions'
import { formatCurrency, formatDate, getPaymentMethodLabel } from '../../utils/formatters'
import TransactionReceipt from '../../components/transactions/TransactionReceipt.vue'

const route = useRoute()
const transaction = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await getTransaction(route.params.id)
    transaction.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})
</script>
