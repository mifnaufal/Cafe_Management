export function required(value) {
  if (!value || (typeof value === 'string' && !value.trim())) return 'Wajib diisi'
  return ''
}

export function email(value) {
  if (!value) return ''
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) ? '' : 'Email tidak valid'
}

export function minLength(min) {
  return (value) => {
    if (value && value.length < min) return `Minimal ${min} karakter`
    return ''
  }
}

export function positiveNumber(value) {
  if (value === '' || value === null || value === undefined) return 'Wajib diisi'
  if (Number(value) < 0) return 'Tidak boleh negatif'
  return ''
}
