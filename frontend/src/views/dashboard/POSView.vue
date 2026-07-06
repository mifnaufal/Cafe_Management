<template>
  <div class="pos-layout">
    <div class="pos-products">
      <div class="flex gap-3" style="margin-bottom: 1rem;">
        <input v-model="search" class="input" placeholder="Cari produk..." @input="debounceSearch" />
        <select v-model="filterCategory" class="input" style="max-width: 200px;" @change="fetchProducts">
          <option :value="null">Semua Kategori</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
      </div>
      <div v-if="loading" class="loading"><div class="spinner" /></div>
      <div v-else class="product-grid">
        <div
          v-for="p in products"
          :key="p.id"
          class="product-card"
          :class="{ disabled: p.stock <= 0 }"
          @click="addToCart(p)"
        >
          <div class="product-name">{{ p.name }}</div>
          <div class="product-price">{{ formatCurrency(p.price) }}</div>
          <div class="product-stock" :class="{ low: p.stock <= 5 }">Stok: {{ p.stock }}</div>
        </div>
        <div v-if="!products.length" class="empty-state" style="grid-column: 1 / -1;"><p>Produk tidak ditemukan</p></div>
      </div>
    </div>
    <div class="pos-cart">
      <Cart @checkout="showCheckout = true" />
    </div>
    <CheckoutModal v-if="showCheckout" @close="showCheckout = false" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getProducts } from '../../api/products'
import { getCategories } from '../../api/categories'
import { useCartStore } from '../../stores/cart'
import { formatCurrency } from '../../utils/formatters'
import Cart from '../../components/pos/Cart.vue'
import CheckoutModal from '../../components/pos/CheckoutModal.vue'

const cart = useCartStore()
const products = ref([])
const categories = ref([])
const search = ref('')
const filterCategory = ref(null)
const loading = ref(true)
const showCheckout = ref(false)

let debounceTimer

function debounceSearch() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(fetchProducts, 300)
}

async function fetchProducts() {
  loading.value = true
  try {
    const params = { limit: 100, in_stock_only: false }
    if (search.value) params.search = search.value
    if (filterCategory.value) params.category_id = filterCategory.value
    const { data } = await getProducts(params)
    products.value = data.items || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function addToCart(product) {
  if (product.stock <= 0) return
  cart.addItem(product)
}

onMounted(async () => {
  try {
    const { data } = await getCategories()
    categories.value = data || []
  } catch (e) { /* ignore */ }
  await fetchProducts()
})
</script>

<style scoped>
.pos-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 1.5rem;
  height: calc(100vh - var(--navbar-height) - 3rem);
}
.pos-products {
  overflow-y: auto;
}
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 0.75rem;
}
.product-card {
  background: #fff;
  border: 1px solid var(--gray-200);
  border-radius: var(--radius);
  padding: 1rem;
  cursor: pointer;
  transition: all 0.15s;
}
.product-card:hover { border-color: var(--primary); box-shadow: 0 2px 8px rgba(79,70,229,0.1); }
.product-card.disabled { opacity: 0.5; cursor: not-allowed; }
.product-name { font-weight: 600; font-size: 0.875rem; margin-bottom: 0.25rem; }
.product-price { color: var(--primary); font-weight: 600; font-size: 1rem; }
.product-stock { font-size: 0.75rem; color: var(--gray-400); margin-top: 0.25rem; }
.product-stock.low { color: var(--danger); }
.pos-cart {
  overflow-y: auto;
}
</style>
