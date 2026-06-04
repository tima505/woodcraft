<template>
  <div>
    <div class="page-header">
      <h2>Продукты и Этапы</h2>
      <button class="btn-primary" @click="openModal">Создать продукт</button>
    </div>

    <div class="products-list">
      <div class="card product-card" v-for="product in productsStore.products" :key="product.id">
        <div class="product-header">
          <h3>{{ product.name }}</h3>
          <div class="actions">
            <button class="btn-edit" @click="handleEdit(product)">Редактировать</button>
            <button class="btn-delete" @click="handleDelete(product.id)">Удалить</button>
          </div>
        </div>
        <p class="desc">{{ product.description }}</p>
        
        <div class="stages-flow">
          <span v-for="(stage, idx) in product.stages" :key="stage.id">
            <span class="stage-badge">{{ stage.name }}</span>
            <span v-if="idx < product.stages.length - 1" class="arrow">→</span>
          </span>
        </div>
      </div>
    </div>

    <!-- Modal for new product -->
    <div class="modal-backdrop" v-if="showModal" @click.self="showModal = false">
      <div class="modal-content-container standard v-if-anim">
        <div class="modal-header">
          <h2>{{ editMode ? 'Редактировать продукт' : 'Новый продукт' }}</h2>
          <button class="close-btn" @click="closeModal">✕</button>
        </div>
        <form @submit.prevent="submitProduct">
          <div class="form-group">
            <label>Название</label>
            <input type="text" v-model="formData.name" required />
          </div>
          <div class="form-group">
            <label>Описание</label>
            <textarea v-model="formData.description" rows="2"></textarea>
          </div>
          
          <div class="stages-config">
            <h4>Этапы производства</h4>
            
            <!-- Выбранные этапы (в порядке) -->
            <div v-if="formData.stages.length" class="selected-stages">
              <div class="stage-input-row" v-for="(stageName, i) in formData.stages" :key="i">
                <span class="stage-order">{{ i + 1 }}.</span>
                <span class="stage-selected-name">{{ stageName }}</span>
                <div class="stage-row-actions">
                  <button type="button" @click="moveStageUp(i)" class="btn-move" :disabled="i === 0" title="Вверх">↑</button>
                  <button type="button" @click="moveStageDown(i)" class="btn-move" :disabled="i === formData.stages.length - 1" title="Вниз">↓</button>
                  <button type="button" @click="removeStage(i)" class="btn-remove">✕</button>
                </div>
              </div>
            </div>
            <p v-else class="no-stages-hint">Выберите этапы из списка ниже</p>

            <!-- Доступные этапы для выбора -->
            <div class="available-stages">
              <div 
                v-for="tmpl in availableTemplates" 
                :key="tmpl.id" 
                class="available-stage-item"
                @click="addStageFromTemplate(tmpl.name)"
              >
                <span>+ {{ tmpl.name }}</span>
              </div>
              <p v-if="!stageTemplatesStore.stageTemplates.length" class="no-templates-hint">
                Нет доступных этапов. <router-link to="/settings">Создать в настройках</router-link>
              </p>
              <p v-else-if="!availableTemplates.length" class="no-templates-hint">
                Все этапы уже добавлены
              </p>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" @click="closeModal" class="btn-cancel">Отмена</button>
            <button type="submit" class="btn-primary" :disabled="!formData.stages.length">Сохранить</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useProductsStore } from '../stores/products'
import { useStageTemplatesStore } from '../stores/stageTemplates'

const productsStore = useProductsStore()
const stageTemplatesStore = useStageTemplatesStore()
const showModal = ref(false)
const editMode = ref(false)
const editingId = ref(null)

const formData = ref({
  name: '',
  description: '',
  stages: []
})

onMounted(async () => {
  await productsStore.fetchProducts()
  await stageTemplatesStore.fetchStageTemplates()
})

const availableTemplates = computed(() => {
  return stageTemplatesStore.stageTemplates.filter(
    t => !formData.value.stages.includes(t.name)
  )
})

const closeModal = () => {
  showModal.value = false
  editMode.value = false
  editingId.value = null
  formData.value = { name: '', description: '', stages: [] }
}

const openModal = () => {
  closeModal()
  showModal.value = true
}

const handleEdit = (product) => {
  editMode.value = true
  editingId.value = product.id
  formData.value = {
    name: product.name,
    description: product.description,
    stages: product.stages.map(s => s.name)
  }
  showModal.value = true
}

const addStageFromTemplate = (name) => {
  if (!formData.value.stages.includes(name)) {
    formData.value.stages.push(name)
  }
}

const removeStage = (idx) => {
  formData.value.stages.splice(idx, 1)
}

const moveStageUp = (idx) => {
  if (idx > 0) {
    const tmp = formData.value.stages[idx]
    formData.value.stages[idx] = formData.value.stages[idx - 1]
    formData.value.stages[idx - 1] = tmp
  }
}

const moveStageDown = (idx) => {
  if (idx < formData.value.stages.length - 1) {
    const tmp = formData.value.stages[idx]
    formData.value.stages[idx] = formData.value.stages[idx + 1]
    formData.value.stages[idx + 1] = tmp
  }
}

const submitProduct = async () => {
  try {
    if (editMode.value) {
      await productsStore.updateProduct(editingId.value, formData.value)
    } else {
      await productsStore.createProduct(formData.value)
    }
    closeModal()
  } catch(e) {
    alert('Ошибка при сохранении')
  }
}

const handleDelete = async (id) => {
  if(confirm('Точно удалить продукт?')) {
    await productsStore.deleteProduct(id)
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
.products-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}
.product-card {
  padding: 24px;
}
.product-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.product-header h3 {
  font-size: 1.15rem;
}
.actions {
  display: flex;
  gap: 8px;
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
.btn-edit:hover {
  background: var(--border-color);
}
.btn-delete {
  background: transparent;
  color: var(--color-overdue);
  border: 1px solid var(--color-overdue);
  padding: 6px 12px;
  font-size: 0.85rem;
  font-weight: 600;
  transition: all var(--transition-speed) ease;
}
.btn-delete:hover {
  background: var(--color-overdue);
  color: #FFF;
}
.desc {
  color: var(--text-muted);
  margin-bottom: 20px;
  font-size: 0.95rem;
  line-height: 1.5;
}
.stages-flow {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
}
.stage-badge {
  background: var(--bg-color);
  padding: 6px 12px;
  border-radius: var(--radius-badge);
  font-size: 0.85rem;
  font-weight: 600;
  border: 1px solid var(--border-color);
}
.arrow {
  color: var(--text-muted);
  font-weight: 600;
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
.stages-config {
  background: var(--bg-color);
  padding: 20px;
  border-radius: var(--radius-btn);
  margin-bottom: 24px;
  border: 1px solid var(--border-color);
}
.stages-config h4 { 
  margin-bottom: 16px; 
  font-size: 0.95rem;
}
.selected-stages {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}
.stage-input-row {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--card-bg);
  padding: 10px 14px;
  border-radius: var(--radius-btn);
  border: 1px solid var(--border-color);
}
.stage-order {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-muted);
  width: 20px;
}
.stage-selected-name {
  flex: 1;
  font-weight: 600;
  font-size: 0.95rem;
}
.stage-row-actions {
  display: flex;
  align-items: center;
  gap: 4px;
}
.btn-move {
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  border-radius: 4px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  transition: all var(--transition-speed) ease;
}
.btn-move:hover:not(:disabled) {
  background: var(--border-color);
  color: var(--text-main);
}
.btn-move:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}
.btn-remove {
  background: none; 
  border: none; 
  color: var(--color-overdue); 
  font-size: 1.2rem;
  cursor: pointer;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}
.btn-remove:hover {
  background: rgba(226, 75, 74, 0.1);
}
.available-stages {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px dashed var(--border-color);
}
.available-stage-item {
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  padding: 6px 12px;
  border-radius: var(--radius-badge);
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-speed) ease;
}
.available-stage-item:hover {
  background: var(--card-bg);
  border-color: var(--accent-color);
  color: var(--accent-color);
}
.no-stages-hint {
  color: var(--text-muted);
  font-size: 0.85rem;
  font-style: italic;
  margin-bottom: 16px;
}
.no-templates-hint {
  color: var(--text-muted);
  font-size: 0.85rem;
  width: 100%;
}
.no-templates-hint a {
  text-decoration: underline;
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
