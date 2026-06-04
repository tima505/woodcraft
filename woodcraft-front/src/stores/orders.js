import { defineStore } from 'pinia'
import api from '../utils/api'

export const useOrdersStore = defineStore('orders', {
  state: () => ({
    orders: [],
    dashboardTasks: []
  }),
  actions: {
    async fetchOrders() {
      const res = await api.get('orders/')
      this.orders = res.data
    },
    async createOrder(orderData) {
      const res = await api.post('orders/', orderData)
      this.orders.unshift(res.data)
      return res.data
    },
    async getOrder(id) {
      const res = await api.get(`orders/${id}/`)
      return res.data
    },
    async updateItemStage(stageId, data) {
      await api.patch(`item-stages/${stageId}/`, data)
    },
    async fetchDashboardTasks() {
      const res = await api.get('dashboard/')
      this.dashboardTasks = res.data
    },
    async completeStage(stageId) {
      await api.post('stage/complete/', { item_stage_id: stageId })
      await this.fetchDashboardTasks()
    },
    async returnStage(stageId, note) {
      await api.post('stage/return-back/', { item_stage_id: stageId, note })
      await this.fetchDashboardTasks()
    }
  }
})
