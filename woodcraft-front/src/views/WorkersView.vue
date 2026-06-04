<template>
  <div>
    <div class="page-header">
      <h2>Рабочие</h2>
      <button class="btn-primary" @click="showModal = true">Добавить рабочего</button>
    </div>

    <div class="workers-grid">
      <div class="card worker-card" v-for="worker in workersStore.workers" :key="worker.id">
        <button class="btn-delete abs-delete" @click="handleDelete(worker.id)">Удалить</button>
        <div class="worker-header">
          <div class="avatar">{{ (worker.user?.first_name || worker.user?.username || '?').charAt(0).toUpperCase() }}</div>
          <div class="info">
            <h3>{{ worker.user?.first_name || worker.user?.username }}</h3>
            <span class="username">@{{ worker.user?.username }}</span>
          </div>
        </div>
        
        <div class="stages-assigned">
          <span class="stage-tag" v-for="st in worker.stages" :key="st.id">{{ st.name }}</span>
        </div>

        <div class="worker-footer">
          <button class="btn-edit full-width" @click="handleEdit(worker)">Редактировать</button>
        </div>
      </div>
    </div>

    <!-- Modal for new worker -->
    <div class="modal-backdrop" v-if="showModal" @click.self="showModal = false">
      <div class="modal-content-container standard v-if-anim">
        <div class="modal-header">
          <h2>{{ editMode ? 'Редактировать рабочего' : 'Новый рабочий' }}</h2>
          <button class="close-btn" @click="closeModal">✕</button>
        </div>
        <form @submit.prevent="submitWorker">
          <div class="form-group">
            <label>Имя</label>
            <input type="text" v-model="formData.first_name" required />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Логин</label>
              <input type="text" v-model="formData.username" required />
            </div>
            <div class="form-group">
              <label>Пароль</label>
              <input type="password" v-model="formData.password" :required="!editMode" :placeholder="editMode ? 'Оставьте пустым, чтобы не менять' : ''" />
            </div>
          </div>
          
          <div class="stages-selection">
            <h4>Разрешенные этапы</h4>
            <div class="checkbox-grid global-stages-grid">
              <label v-for="st in stageTemplatesStore.stageTemplates" :key="st.id" class="checkbox-label">
                <input type="checkbox" :value="st.id" v-model="formData.stage_ids" />
                {{ st.name }}
              </label>
            </div>
            <p v-if="stageTemplatesStore.stageTemplates.length === 0" class="text-muted" style="font-size: 0.85rem; margin-top: 10px;">
              Нет доступных этапов. Создайте их в настройках.
            </p>
          </div>

          <div class="form-actions">
            <button type="button" @click="closeModal" class="btn-cancel">Отмена</button>
            <button type="submit" class="btn-primary">Сохранить</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useWorkersStore } from '../stores/workers'
import { useStageTemplatesStore } from '../stores/stageTemplates'

const workersStore = useWorkersStore()
const stageTemplatesStore = useStageTemplatesStore()
const showModal = ref(false)
const editMode = ref(false)
const editingId = ref(null)

const formData = ref({
  first_name: '',
  username: '',
  password: '',
  stage_ids: []
})

const closeModal = () => {
  showModal.value = false
  editMode.value = false
  editingId.value = null
  formData.value = { first_name: '', username: '', password: '', stage_ids: [] }
}

const handleEdit = (worker) => {
  editMode.value = true
  editingId.value = worker.id
  formData.value = {
    first_name: worker.user?.first_name || '',
    username: worker.user?.username || '',
    password: '',
    stage_ids: worker.stages.map(s => s.id)
  }
  showModal.value = true
}

onMounted(async () => {
  await workersStore.fetchWorkers()
  if (stageTemplatesStore.stageTemplates.length === 0) {
    await stageTemplatesStore.fetchStageTemplates()
  }
})

const submitWorker = async () => {
  try {
    if (editMode.value) {
      await workersStore.updateWorker(editingId.value, formData.value)
    } else {
      await workersStore.createWorker(formData.value)
    }
    closeModal()
  } catch(e) {
    alert('Ошибка. Возможно логин занят или данные неверны.')
  }
}

const handleDelete = async (id) => {
  if(confirm('Удалить рабочего?')) {
    await workersStore.deleteWorker(id)
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
.workers-grid {
  display: grid; 
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); 
  gap: 20px;
}
.worker-card { 
  padding: 20px; 
  position: relative;
  display: flex;
  flex-direction: column;
}
.abs-delete {
  position: absolute;
  top: 15px;
  right: 15px;
}
.worker-footer {
  margin-top: auto;
  padding-top: 15px;
}
.worker-header { 
  display: flex; 
  align-items: center; 
  gap: 15px; 
  margin-bottom: 15px; 
  padding-right: 40px; /* space for absolute delete button */
}
.avatar {
  width: 44px; 
  height: 44px; 
  flex-shrink: 0;
  border-radius: 50%; 
  background: var(--accent-color); 
  color: var(--card-bg);
  display: flex; 
  justify-content: center; 
  align-items: center; 
  font-size: 1.1rem; 
  font-weight: bold;
}
.btn-edit {
  background: transparent;
  color: var(--text-main);
  border: 1px solid var(--border-color);
  padding: 6px 12px;
  font-size: 0.85rem;
  font-weight: 600;
  transition: all var(--transition-speed) ease;
}
.btn-edit.full-width {
  width: 100%;
  padding: 8px;
}
.btn-edit:hover {
  background: var(--border-color);
}
.info { 
  flex: 1; 
}
.info h3 { 
  margin: 0; 
  font-size: 1.05rem; 
}
.username { 
  color: var(--text-muted); 
  font-size: 0.85rem; 
}
.btn-delete { 
  background: none; 
  border: none; 
  color: var(--color-overdue); 
  cursor: pointer; 
  font-size: 0.85rem;
  font-weight: 600;
}
.btn-delete:hover {
  text-decoration: underline;
}
.stages-assigned { 
  display: flex; 
  flex-wrap: wrap; 
  gap: 8px; 
}
.stage-tag {
  background: var(--bg-color); 
  padding: 4px 10px; 
  border-radius: var(--radius-badge); 
  font-size: 0.8rem; 
  font-weight: 500;
  border: 1px solid var(--border-color);
}
.modal-content-container.standard {
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
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
  margin-bottom: 16px; 
}
.form-group label { 
  display: block; 
  margin-bottom: 6px; 
  font-size: 0.85rem;
  font-weight: 600;
}
.form-row { 
  display: flex; 
  gap: 15px; 
}
.form-row .form-group { 
  flex: 1; 
}
.stages-selection {
  background: var(--bg-color); 
  padding: 20px; 
  border-radius: var(--radius-btn); 
  margin-bottom: 24px;
  border: 1px solid var(--border-color);
  max-height: 240px;
  overflow-y: auto;
}
.stages-selection h4 {
  margin-bottom: 12px;
  font-size: 0.95rem;
}
.product-group { 
  margin-bottom: 15px; 
}
.checkbox-grid { 
  display: grid; 
  grid-template-columns: 1fr 1fr; 
  gap: 10px; 
  margin-top: 8px; 
}
.checkbox-label { 
  display: flex; 
  align-items: center; 
  gap: 8px; 
  font-size: 0.85rem; 
  cursor: pointer; 
  color: var(--text-main);
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
