import { defineStore } from 'pinia'
import api from '../utils/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    isAdmin: false
  }),
  getters: {
    isAuthenticated: (state) => !!state.token
  },
  actions: {
    async login(username, password) {
      const res = await api.post('auth/login/', { username, password })
      this.token = res.data.token
      this.isAdmin = res.data.is_admin
      localStorage.setItem('token', this.token)
      await this.fetchUser()
    },
    async fetchUser() {
      if (!this.token) return
      try {
        const res = await api.get('me/')
        this.user = res.data
        this.isAdmin = res.data.is_admin
      } catch (err) {
        this.logout()
      }
    },
    async logout() {
      try {
        if (this.token) await api.post('auth/logout/')
      } catch (e) {}
      this.user = null
      this.token = null
      this.isAdmin = false
      localStorage.removeItem('token')
    }
  }
})
