<template>
  <div>
    <div class="page-header">
      <h2>Настройки</h2>
    </div>

    <div class="settings-section">
      <div class="section-header">
        <div>
          <h3>Этапы производства</h3>
          <p class="section-desc">Создайте этапы, которые можно будет назначать продуктам</p>
        </div>
        <button class="btn-primary" @click="showModal = true">+ Новый этап</button>
      </div>

      <div class="stages-list" v-if="stageTemplatesStore.stageTemplates.length">
        <div class="stage-item card" v-for="stage in stageTemplatesStore.stageTemplates" :key="stage.id">
          <div class="stage-item-content">
            <div class="stage-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>
            </div>
            <div class="stage-info">
              <template v-if="editingId === stage.id">
                <input 
                  type="text" 
                  v-model="editingName" 
                  @keyup.enter="saveEdit(stage.id)"
                  @keyup.escape="cancelEdit"
                  class="edit-input"
                  ref="editInput"
                />
              </template>
              <template v-else>
                <span class="stage-name">{{ stage.name }}</span>
              </template>
            </div>
          </div>
          <div class="stage-actions">
            <template v-if="editingId === stage.id">
              <button class="btn-icon btn-save" @click="saveEdit(stage.id)" title="Сохранить">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
              </button>
              <button class="btn-icon btn-cancel-edit" @click="cancelEdit" title="Отмена">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
              </button>
            </template>
            <template v-else>
              <button class="btn-icon btn-edit" @click="startEdit(stage)" title="Редактировать">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
              </button>
              <button class="btn-icon btn-delete-icon" @click="handleDelete(stage.id)" title="Удалить">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
              </button>
            </template>
          </div>
        </div>
      </div>

      <div class="empty-state" v-else>
        <div class="empty-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>
        </div>
        <p>Этапы ещё не созданы</p>
        <span>Создайте этапы производства для использования в продуктах</span>
      </div>
    </div>

    <!-- Modal для нового этапа -->
    <div class="modal-backdrop" v-if="showModal" @click.self="showModal = false">
      <div class="modal-content-container standard v-if-anim">
        <div class="modal-header">
          <h2>Новый этап</h2>
          <button class="close-btn" @click="showModal = false">✕</button>
        </div>
        <form @submit.prevent="submitStage">
          <div class="form-group">
            <label>Название этапа</label>
            <input type="text" v-model="newStageName" required placeholder="Например: Заготовка, Сборка, Покраска..." />
          </div>
          <div class="form-actions">
            <button type="button" @click="showModal = false" class="btn-cancel">Отмена</button>
            <button type="submit" class="btn-primary" :disabled="!newStageName.trim()">Создать</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStageTemplatesStore } from '../stores/stageTemplates'

const stageTemplatesStore = useStageTemplatesStore()
const showModal = ref(false)
const newStageName = ref('')
const editingId = ref(null)
const editingName = ref('')

onMounted(async () => {
  await stageTemplatesStore.fetchStageTemplates()
})

const submitStage = async () => {
  if (!newStageName.value.trim()) return
  try {
    await stageTemplatesStore.createStageTemplate(newStageName.value.trim())
    showModal.value = false
    newStageName.value = ''
  } catch (e) {
    alert('Ошибка. Возможно, этап с таким названием уже существует.')
  }
}

const startEdit = (stage) => {
  editingId.value = stage.id
  editingName.value = stage.name
}

const cancelEdit = () => {
  editingId.value = null
  editingName.value = ''
}

const saveEdit = async (id) => {
  if (!editingName.value.trim()) return
  try {
    await stageTemplatesStore.updateStageTemplate(id, editingName.value.trim())
    cancelEdit()
  } catch (e) {
    alert('Ошибка при обновлении')
  }
}

const handleDelete = async (id) => {
  if (confirm('Удалить этот этап?')) {
    await stageTemplatesStore.deleteStageTemplate(id)
  }
}
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.settings-section {
  background-color: var(--card-bg);
  border-radius: var(--radius-card);
  border: 1px solid var(--border-color);
  padding: 28px;
  transition: background-color var(--transition-speed) ease, border-color var(--transition-speed) ease;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.section-header h3 {
  font-size: 1.1rem;
  margin-bottom: 4px;
}

.section-desc {
  color: var(--text-muted);
  font-size: 0.85rem;
}

.stages-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stage-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  transition: all var(--transition-speed) ease;
}

.stage-item:hover {
  transform: none;
  border-color: var(--text-muted);
}

.stage-item-content {
  display: flex;
  align-items: center;
  gap: 14px;
  flex: 1;
}

.stage-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background-color: var(--bg-color);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  flex-shrink: 0;
}

.stage-info {
  flex: 1;
}

.stage-name {
  font-weight: 600;
  font-size: 0.95rem;
}

.edit-input {
  padding: 6px 10px;
  font-size: 0.95rem;
  max-width: 300px;
}

.stage-actions {
  display: flex;
  align-items: center;
  gap: 4px;
}

.btn-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  transition: all var(--transition-speed) ease;
}

.btn-icon:hover {
  background-color: var(--bg-color);
  color: var(--text-main);
}

.btn-delete-icon:hover {
  background-color: rgba(226, 75, 74, 0.1);
  color: var(--color-overdue);
}

.btn-save:hover {
  background-color: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.empty-state {
  text-align: center;
  padding: 48px 20px;
}

.empty-icon {
  color: var(--border-color);
  margin-bottom: 16px;
}

.empty-state p {
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 6px;
}

.empty-state span {
  color: var(--text-muted);
  font-size: 0.85rem;
}

/* Modal */
.modal-content-container.standard {
  max-width: 450px;
  padding: 30px;
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.modal-header h2 {
  font-size: 1.3rem;
  margin: 0;
}
.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--text-muted);
  line-height: 1;
}
.close-btn:hover {
  color: var(--text-main);
}
.form-group {
  margin-bottom: 20px;
}
.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 0.85rem;
  font-weight: 600;
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid var(--border-color);
  padding-top: 20px;
}
.btn-cancel {
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  padding: 10px 18px;
  color: var(--text-main);
  font-weight: 500;
  transition: all var(--transition-speed) ease;
}
.btn-cancel:hover {
  background-color: var(--border-color);
}
</style>
