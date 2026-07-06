<template>
  <div>
    <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); margin-bottom: 1.5rem;">
      <SummaryCard title="Penjualan Hari Ini" :amount="summary.today?.total_sales || 0" :subtitle="`${summary.today?.total_transactions || 0} transaksi`" />
      <SummaryCard title="Penjualan Minggu Ini" :amount="summary.this_week?.total_sales || 0" :subtitle="`${summary.this_week?.total_transactions || 0} transaksi`" />
      <SummaryCard title="Penjualan Bulan Ini" :amount="summary.this_month?.total_sales || 0" :subtitle="`${summary.this_month?.total_transactions || 0} transaksi`" />
      <SummaryCard title="Rata-rata Transaksi" :amount="Math.round(summary.today?.average_transaction || 0)" subtitle="Hari ini" />
    </div>

    <div class="grid" style="grid-template-columns: 2fr 1fr;">
      <div class="card">
        <h3 style="margin-bottom: 1rem; font-size: 1rem;">Grafik Penjualan (7 Hari)</h3>
        <SalesChart :data="salesData" />
      </div>
      <div class="card">
        <h3 style="margin-bottom: 1rem; font-size: 1rem;">Kategori</h3>
        <CategoryPieChart :data="categoryData" />
      </div>
    </div>

    <div class="card" style="margin-top: 1.5rem;">
      <div class="flex justify-between items-center" style="margin-bottom: 1rem;">
        <h3 style="font-size: 1rem;">Produk Terlaris</h3>
      </div>
      <table class="table" v-if="topProducts.length">
        <thead>
          <tr>
            <th>Produk</th>
            <th>Terjual</th>
            <th class="text-right">Total</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in topProducts" :key="p.product_id">
            <td>{{ p.product_name }}</td>
            <td>{{ p.total_quantity }}</td>
            <td class="text-right">{{ formatCurrency(p.total_sales) }}</td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state"><p>Belum ada data penjualan</p></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getSummary, getSalesChart, getTopProducts, getCategoryBreakdown } from '../../api/reports'
import { formatCurrency } from '../../utils/formatters'
import SummaryCard from '../../components/dashboard/SummaryCard.vue'
import SalesChart from '../../components/dashboard/SalesChart.vue'
import CategoryPieChart from '../../components/dashboard/CategoryPieChart.vue'

const summary = ref({})
const salesData = ref([])
const topProducts = ref([])
const categoryData = ref([])

async function fetchData() {
  try {
    const [s, sc, tp, cb] = await Promise.all([
      getSummary(), getSalesChart(), getTopProducts(), getCategoryBreakdown(),
    ])
    summary.value = s.data
    salesData.value = sc.data || []
    topProducts.value = tp.data || []
    categoryData.value = cb.data || []
  } catch (e) {
    console.error('Failed to load dashboard data', e)
  }
}

onMounted(fetchData)
</script>
