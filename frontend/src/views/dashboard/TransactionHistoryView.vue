<template>
  <div>
    <div class="flex justify-between items-center" style="margin-bottom: 1.5rem;">
      <h2 style="font-size: 1.25rem; font-weight: 600;">Riwayat Transaksi</h2>
    </div>

    <div v-if="loading" class="loading"><div class="spinner" /></div>
    <div v-else>
      <table class="table">
        <thead>
          <tr>
            <th>No. Transaksi</th>
            <th>Tanggal</th>
            <th>Total</th>
            <th>Pembayaran</th>
            <th>Kasir</th>
            <th>Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in transactions" :key="t.id">
            <td><strong>{{ t.transaction_number }}</strong></td>
            <td>{{ formatDate(t.created_at) }}</td>
            <td>{{ formatCurrency(t.total_amount) }}</td>
            <td><span class="badge badge-gray">{{ getPaymentMethodLabel(t.payment_method) }}</span></td>
            <td>{{ t.cashier?.full_name || '-' }}</td>
            <td>
              <routerLink :to="`/transactions/${t.id}`" class="btn btn-secondary btn-sm">Detail</routerLink>
            </td>
          </tr>
          <tr v-if="!transactions.length">
            <td colspan="6" class="empty-state"><p>Belum ada transaksi</p></td>
          </tr>
        </tbody>
      </table>

      <div class="pagination" v-if="totalPages > 1">
        <button :disabled="page <= 1" @click="goTo(page - 1)">Prev</button>
        <button v-for="p in totalPages" :key="p" :class="{ active: p === page }" @click="goTo(p)">{{ p }}</button>
        <button :disabled="page >= totalPages" @click="goTo(page + 1)">Next</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTransactions } from '../../api/transactions'
import { formatCurrency, formatDate, getPaymentMethodLabel } from '../../utils/formatters'

const transactions = ref([])
const loading = ref(true)
const page = ref(1)
const totalPages = ref(1)

async function fetchTransactions() {
  loading.value = true
  try {
    const { data } = await getTransactions({ page: page.value, limit: 10 })
    transactions.value = data.items || []
    totalPages.value = data.total_pages || 1
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function goTo(p) {
  page.value = p
  fetchTransactions()
}

onMounted(fetchTransactions)
</script>
