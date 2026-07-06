import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])

  const totalItems = computed(() => items.value.reduce((sum, i) => sum + i.quantity, 0))
  const totalPrice = computed(() => items.value.reduce((sum, i) => sum + i.subtotal, 0))
  const isEmpty = computed(() => items.value.length === 0)

  function addItem(product) {
    const existing = items.value.find((i) => i.product_id === product.id)
    if (existing) {
      existing.quantity += 1
      existing.subtotal = existing.quantity * existing.price_at_time
    } else {
      items.value.push({
        product_id: product.id,
        product_name: product.name,
        price_at_time: product.price,
        quantity: 1,
        subtotal: product.price,
        stock: product.stock,
      })
    }
  }

  function updateQuantity(productId, qty) {
    const item = items.value.find((i) => i.product_id === productId)
    if (!item) return
    if (qty <= 0) {
      removeItem(productId)
      return
    }
    item.quantity = qty
    item.subtotal = qty * item.price_at_time
  }

  function removeItem(productId) {
    items.value = items.value.filter((i) => i.product_id !== productId)
  }

  function clear() {
    items.value = []
  }

  return { items, totalItems, totalPrice, isEmpty, addItem, updateQuantity, removeItem, clear }
})
