<template>
  <table class="table">
    <thead>
      <tr>
        <th>No. Transaksi</th>
        <th>Tanggal</th>
        <th class="text-right">Total</th>
        <th>Pembayaran</th>
        <th>Kasir</th>
        <th>Aksi</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="t in transactions" :key="t.id">
        <td><strong>{{ t.transaction_number }}</strong></td>
        <td>{{ formatDate(t.created_at) }}</td>
        <td class="text-right">{{ formatCurrency(t.total_amount) }}</td>
        <td><span class="badge badge-gray">{{ getPaymentMethodLabel(t.payment_method) }}</span></td>
        <td>{{ t.cashier?.full_name || '-' }}</td>
        <td>
          <router-link :to="`/transactions/${t.id}`" class="btn btn-secondary btn-sm">Detail</router-link>
        </td>
      </tr>
      <tr v-if="!transactions.length">
        <td colspan="6" class="empty-state"><p>Belum ada transaksi</p></td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
import { formatCurrency, formatDate, getPaymentMethodLabel } from '../../utils/formatters'
defineProps({ transactions: { type: Array, default: () => [] } })
</script>
