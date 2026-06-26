import axios from 'axios'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
})

export const productsApi = {
  list:        ()            => http.get('/products/'),
  get:         (sku)         => http.get(`/products/${sku}`),
  create:      (data)        => http.post('/products/', data),
  updateStock: (sku, qty)    => http.put(`/products/${sku}/stock`, { quantity: qty }),
  delete:      (sku)         => http.delete(`/products/${sku}`),
}

export const ticketsApi = {
  list:         ()           => http.get('/tickets/'),
  get:          (id)         => http.get(`/tickets/${id}`),
  create:       (data)       => http.post('/tickets/', data),
  updateStatus: (id, status) => http.put(`/tickets/${id}/status`, { status }),
  delete:       (id)         => http.delete(`/tickets/${id}`),
}

export const customersApi = {
  list:    ()     => http.get('/customers/'),
  get:     (id)   => http.get(`/customers/${id}`),
  create:  (data) => http.post('/customers/', data),
  tickets: (id)   => http.get(`/customers/${id}/tickets`),
  delete:  (id)   => http.delete(`/customers/${id}`),
}

export const alertsApi = {
  check: () => http.get('/alerts/'),
}
