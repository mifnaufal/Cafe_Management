export function formatCurrency(amount) {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount)
}

export function formatDate(dateStr) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('id-ID', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function formatDateShort(dateStr) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('id-ID', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

export function formatNumber(num) {
  return new Intl.NumberFormat('id-ID').format(num)
}

export function getRoleBadgeClass(role) {
  return role === 'admin' ? 'badge-success' : 'badge-gray'
}

export function getPaymentMethodLabel(method) {
  const labels = { cash: 'Tunai', card: 'Kartu', ewallet: 'E-Wallet' }
  return labels[method] || method
}
