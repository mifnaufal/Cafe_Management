<template>
  <form @submit.prevent="$emit('save', form)">
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
      <p v-if="error" class="form-error">{{ error }}</p>
    </div>
    <div class="modal-footer">
      <button type="button" class="btn btn-secondary" @click="$emit('cancel')">Batal</button>
      <button type="submit" class="btn btn-primary" :disabled="saving">{{ saving ? 'Menyimpan...' : 'Simpan' }}</button>
    </div>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
defineProps({ product: Object, categories: { type: Array, default: () => [] }, editing: Boolean, saving: Boolean, error: String })
defineEmits(['save', 'cancel'])

const form = reactive({ ...product })
</script>
