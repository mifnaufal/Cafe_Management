<template>
  <table class="table">
    <thead><tr><th v-for="col in columns" :key="col.key" :class="col.class">{{ col.label }}</th></tr></thead>
    <tbody>
      <tr v-for="(row, i) in data" :key="i">
        <td v-for="col in columns" :key="col.key" :class="col.class">
          <slot :name="`cell-${col.key}`" :row="row" :value="row[col.key]">
            {{ row[col.key] }}
          </slot>
        </td>
      </tr>
      <tr v-if="!data.length">
        <td :colspan="columns.length" class="empty-state"><slot name="empty"><p>Tidak ada data</p></slot></td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
defineProps({ columns: { type: Array, default: () => [] }, data: { type: Array, default: () => [] } })
</script>
