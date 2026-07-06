import api from './axios'

export const getSummary = () => api.get('/reports/summary')
export const getSalesChart = (days = 7) => api.get('/reports/sales-chart', { params: { days } })
export const getTopProducts = (limit = 5) => api.get('/reports/top-products', { params: { limit } })
export const getCategoryBreakdown = () => api.get('/reports/category-breakdown')
