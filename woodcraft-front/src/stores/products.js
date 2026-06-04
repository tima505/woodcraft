import { defineStore } from 'pinia'
import api from '../utils/api'

export const useProductsStore = defineStore('products', {
  state: () => ({
    products: [],
    templates: []
  }),
  actions: {
    async fetchProducts() {
      const res = await api.get('products/')
      this.products = res.data
    },
    async createProduct(data) {
      await api.post('products/', data)
      await this.fetchProducts()
    },
    async deleteProduct(id) {
      await api.delete(`products/${id}/`)
      await this.fetchProducts()
    },
    async fetchTemplates() {
      const res = await api.get('templates/')
      this.templates = res.data
    },
    async createTemplate(data) {
      await api.post('templates/', data)
      await this.fetchTemplates()
    },
    async deleteTemplate(id) {
      await api.delete(`templates/${id}/`)
      await this.fetchTemplates()
    },
    async updateProduct(id, data) {
      await api.patch(`products/${id}/`, data)
      await this.fetchProducts()
    },
    async updateTemplate(id, data) {
      await api.patch(`templates/${id}/`, data)
      await this.fetchTemplates()
    }
  }
})
