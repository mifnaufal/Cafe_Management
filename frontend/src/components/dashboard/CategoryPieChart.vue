<template>
  <div>
    <div v-if="!data.length" class="empty-state"><p>Belum ada data</p></div>
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

const colors = ['#4f46e5', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#f97316', '#ec4899']

function renderChart() {
  if (chartInstance) chartInstance.destroy()
  if (!chartRef.value || !props.data.length) return

  const labels = props.data.map((d) => d.category_name)
  const values = props.data.map((d) => d.total_sales)

  chartInstance = new Chart(chartRef.value, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: colors.slice(0, labels.length),
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 12, padding: 12, font: { size: 11 } } },
      },
    },
  })
}

onMounted(renderChart)
watch(() => props.data, renderChart, { deep: true })
</script>
