<template>
  <div>
    <div v-if="!data.length" class="empty-state"><p>Belum ada data penjualan</p></div>
    <canvas ref="chartRef" v-else></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const props = defineProps({ data: { type: Array, default: () => [] } })
const chartRef = ref(null)
let chartInstance = null

function renderChart() {
  if (chartInstance) chartInstance.destroy()
  if (!chartRef.value || !props.data.length) return

  const labels = props.data.map((d) => d.date)
  const sales = props.data.map((d) => d.total_sales)

  chartInstance = new Chart(chartRef.value, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Penjualan',
        data: sales,
        borderColor: '#4f46e5',
        backgroundColor: 'rgba(79, 70, 229, 0.1)',
        fill: true,
        tension: 0.3,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, ticks: { callback: (v) => 'Rp' + v.toLocaleString('id-ID') } },
      },
    },
  })
}

onMounted(renderChart)
watch(() => props.data, renderChart, { deep: true })
</script>
