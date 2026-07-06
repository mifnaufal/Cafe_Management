<template>
  <div>
    <div class="flex justify-between items-center" style="margin-bottom: 1.5rem;">
      <div class="flex gap-3">
        <input v-model="search" class="input" style="width: 250px;" placeholder="Cari produk..." @input="debounceSearch" />
        <select v-model="filterCategory" class="input" style="max-width: 180px;" @change="fetchProducts">
          <option :value="null">Semua Kategori</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
      </div>
      <button v-if="auth.isAdmin" class="btn btn-primary" @click="openModal()">+ Tambah Produk</button>
    </div>

    <div v-if="loading" class="loading"><div class="spinner" /></div>
    <div v-else>
      <table class="table">
        <thead>
          <tr>
            <th>Nama</th>
            <th>Kategori</th>
            <th>Harga</th>
            <th>Stok</th>
            <th>Status</th>
            <th v-if="auth.isAdmin">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in products" :key="p.id">
            <td><strong>{{ p.name }}</strong></td>
            <td>{{ p.category?.name || '-' }}</td>
            <td>{{ formatCurrency(p.price) }}</td>
            <td>
              <span :class="{ 'badge-warning': p.stock <= 5, 'badge-gray': p.stock > 5 }">
                {{ p.stock }}
              </span>
            </td>
            <td><span :class="p.is_active ? 'badge-success' : 'badge-gray'">{{ p.is_active ? 'Aktif' : 'Nonaktif' }}</span></td>
            <td v-if="auth.isAdmin">
              <button class="btn btn-secondary btn-sm" style="margin-right: 0.5rem;" @click="openModal(p)">Edit</button>
              <button class="btn btn-danger btn-sm" @click="confirmDelete(p)">Hapus</button>
            </td>
          </tr>
          <tr v-if="!products.length">
            <td :colspan="auth.isAdmin ? 6 : 5" class="empty-state"><p>Produk tidak ditemukan</p></td>
          </tr>
        </tbody>
      </table>

      <div class="pagination" v-if="totalPages > 1">
        <button :disabled="page <= 1" @click="goTo(page - 1)">Prev</button>
        <button v-for="p in totalPages" :key="p" :class="{ active: p === page }" @click="goTo(p)">{{ p }}</button>
        <button :disabled="page >= totalPages" @click="goTo(page + 1)">Next</button>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ editing ? 'Edit Produk' : 'Tambah Produk' }}</h3>
          <button class="btn btn-secondary btn-sm" @click="closeModal">X</button>
        </div>
        <form @submit.prevent="handleSave">
          <div class="modal-body">
            <div class="form-group">
              <label>Nama Produk</label>
              <input v-model="form.name" class="input" required />
            </div>
            <div class="form-group">
              <label>Deskripsi</label>
              <textarea v-model="form.description" class="input" rows="2" />
            </div>
            <div class="flex gap-3">
              <div class="form-group" style="flex:1">
                <label>Harga (Rp)</label>
                <input v-model.number="form.price" type="number" class="input" min="0" required />
              </div>
              <div class="form-group" style="flex:1">
                <label>Stok</label>
                <input v-model.number="form.stock" type="number" class="input" min="0" required />
              </div>
            </div>
            <div class="form-group">
              <label>Kategori</label>
              <select v-model="form.category_id" class="input">
                <option :value="null">Tanpa Kategori</option>
                <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Image URL</label>
              <input v-model="form.image_url" class="input" placeholder="https://..." />
            </div>
            <div class="form-group" v-if="editing">
              <label class="flex items-center gap-2">
                <input type="checkbox" v-model="form.is_active" />
                Produk Aktif
              </label>
            </div>
            <p v-if="formError" class="form-error">{{ formError }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">Batal</button>
            <button type="submit" class="btn btn-primary" :disabled="saving">{{ saving ? 'Menyimpan...' : 'Simpan' }}</button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showDelete" class="modal-overlay" @click.self="showDelete = false">
      <div class="modal-content">
        <div class="modal-header"><h3>Hapus Produk</h3></div>
        <div class="modal-body">
          <p>Yakin ingin menghapus <strong>{{ deleting?.name }}</strong>?</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showDelete = false">Batal</button>
          <button class="btn btn-danger" :disabled="saving" @click="handleDelete">{{ saving ? 'Menghapus...' : 'Hapus' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { getProducts, createProduct, updateProduct, deleteProduct } from '../../api/products'
import { getCategories } from '../../api/categories'
import { formatCurrency } from '../../utils/formatters'

const auth = useAuthStore()
const products = ref([])
const categories = ref([])
const loading = ref(true)
const page = ref(1)
const totalPages = ref(1)
const search = ref('')
const filterCategory = ref(null)
const showModal = ref(false)
const showDelete = ref(false)
const editing = ref(null)
const deleting = ref(null)
const saving = ref(false)
const formError = ref('')
const form = reactive({ name: '', description: '', price: 0, stock: 0, category_id: null, image_url: '', is_active: true })

let debounceTimer

function debounceSearch() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => { page.value = 1; fetchProducts() }, 300)
}

async function fetchProducts() {
  loading.value = true
  try {
    const params = { page: page.value, limit: 10 }
    if (search.value) params.search = search.value
    if (filterCategory.value) params.category_id = filterCategory.value
    const { data } = await getProducts(params)
    products.value = data.items || []
    totalPages.value = data.total_pages || 1
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function goTo(p) {
  page.value = p
  fetchProducts()
}

function openModal(product) {
  editing.value = product || null
  form.name = product?.name || ''
  form.description = product?.description || ''
  form.price = product?.price || 0
  form.stock = product?.stock || 0
  form.category_id = product?.category_id || null
  form.image_url = product?.image_url || ''
  form.is_active = product?.is_active !== false
  formError.value = ''
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  editing.value = null
}

async function handleSave() {
  saving.value = true
  formError.value = ''
  try {
    if (editing.value) {
      await updateProduct(editing.value.id, form)
    } else {
      await createProduct(form)
    }
    closeModal()
    await fetchProducts()
  } catch (err) {
    formError.value = err.response?.data?.detail || 'Gagal menyimpan'
  } finally {
    saving.value = false
  }
}

function confirmDelete(product) {
  deleting.value = product
  showDelete.value = true
}

async function handleDelete() {
  saving.value = true
  try {
    await deleteProduct(deleting.value.id)
    showDelete.value = false
    await fetchProducts()
  } catch (err) {
    alert(err.response?.data?.detail || 'Gagal menghapus')
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  try {
    const { data } = await getCategories()
    categories.value = data || []
  } catch (e) { /* ignore */ }
  await fetchProducts()
})
</script>
