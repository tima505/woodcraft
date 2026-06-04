import { defineStore } from 'pinia'
import api from '../utils/api'

export const useStageTemplatesStore = defineStore('stageTemplates', {
  state: () => ({
    stageTemplates: []
  }),
  actions: {
    async fetchStageTemplates() {
      const res = await api.get('stage-templates/')
      this.stageTemplates = res.data
    },
    async createStageTemplate(name) {
      await api.post('stage-templates/', { name })
      await this.fetchStageTemplates()
    },
    async deleteStageTemplate(id) {
      await api.delete(`stage-templates/${id}/`)
      await this.fetchStageTemplates()
    },
    async updateStageTemplate(id, name) {
      await api.patch(`stage-templates/${id}/`, { name })
      await this.fetchStageTemplates()
    }
  }
})
