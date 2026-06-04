import { defineStore } from 'pinia'
import api from '../utils/api'

export const useWorkersStore = defineStore('workers', {
  state: () => ({
    workers: []
  }),
  actions: {
    async fetchWorkers() {
      const res = await api.get('workers/')
      this.workers = res.data
    },
    async createWorker(data) {
      await api.post('workers/', data)
      await this.fetchWorkers()
    },
    async deleteWorker(id) {
      await api.delete(`workers/${id}/`)
      await this.fetchWorkers()
    },
    async updateWorker(id, data) {
      // Create a copy and remove empty password if not changing it
      const payload = { ...data }
      if (!payload.password) {
        delete payload.password
      }
      await api.patch(`workers/${id}/`, payload)
      await this.fetchWorkers()
    }
  }
})
