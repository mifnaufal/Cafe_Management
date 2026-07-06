<template>
  <div>
    <div class="flex justify-between items-center" style="margin-bottom: 1.5rem;">
      <h2 style="font-size: 1.25rem; font-weight: 600;">Kategori</h2>
      <button v-if="auth.isAdmin" class="btn btn-primary" @click="openModal()">+ Tambah Kategori</button>
    </div>

    <div v-if="loading" class="loading"><div class="spinner" /></div>
    <div v-else>
      <table class="table">
        <thead>
          <tr>
            <th>Nama</th>
            <th>Deskripsi</th>
            <th v-if="auth.isAdmin">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in categories" :key="c.id">
            <td><strong>{{ c.name }}</strong></td>
            <td>{{ c.description || '-' }}</td>
            <td v-if="auth.isAdmin">
              <button class="btn btn-secondary btn-sm" style="margin-right: 0.5rem;" @click="openModal(c)">Edit</button>
              <button class="btn btn-danger btn-sm" @click="confirmDelete(c)">Hapus</button>
            </td>
          </tr>
          <tr v-if="!categories.length">
            <td :colspan="auth.isAdmin ? 3 : 2" class="empty-state"><p>Belum ada kategori</p></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ editing ? 'Edit Kategori' : 'Tambah Kategori' }}</h3>
          <button class="btn btn-secondary btn-sm" @click="closeModal">X</button>
        </div>
        <form @submit.prevent="handleSave">
          <div class="modal-body">
            <div class="form-group">
              <label>Nama Kategori</label>
              <input v-model="form.name" class="input" placeholder="Nama kategori" required />
            </div>
            <div class="form-group">
              <label>Deskripsi</label>
              <textarea v-model="form.description" class="input" rows="3" placeholder="Opsional" />
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
        <div class="modal-header"><h3>Hapus Kategori</h3></div>
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
import { getCategories, createCategory, updateCategory, deleteCategory } from '../../api/categories'

const auth = useAuthStore()
const categories = ref([])
const loading = ref(true)
const showModal = ref(false)
const showDelete = ref(false)
const editing = ref(null)
const deleting = ref(null)
const saving = ref(false)
const formError = ref('')
const form = reactive({ name: '', description: '' })

async function fetchCategories() {
  try {
    const { data } = await getCategories()
    categories.value = data || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function openModal(cat) {
  editing.value = cat || null
  form.name = cat?.name || ''
  form.description = cat?.description || ''
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
      await updateCategory(editing.value.id, form)
    } else {
      await createCategory(form)
    }
    closeModal()
    await fetchCategories()
  } catch (err) {
    formError.value = err.response?.data?.detail || 'Gagal menyimpan'
  } finally {
    saving.value = false
  }
}

function confirmDelete(cat) {
  deleting.value = cat
  showDelete.value = true
}

async function handleDelete() {
  saving.value = true
  try {
    await deleteCategory(deleting.value.id)
    showDelete.value = false
    await fetchCategories()
  } catch (err) {
    alert(err.response?.data?.detail || 'Gagal menghapus')
  } finally {
    saving.value = false
  }
}

onMounted(fetchCategories)
</script>
