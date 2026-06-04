<template>
  <div>
    <div class="page-header">
      <h2>Шаблоны заказов</h2>
      <button class="btn-primary" @click="showModal = true">Создать шаблон</button>
    </div>

    <div class="templates-grid">
      <div class="card template-card" v-for="temp in productsStore.templates" :key="temp.id">
        <div class="header">
          <h3>{{ temp.name }}</h3>
          <div class="actions">
            <button class="btn-edit" @click="handleEdit(temp)">Редактировать</button>
            <button class="btn-delete" @click="handleDelete(temp.id)">Удалить</button>
          </div>
        </div>
        <p class="product-name">Продукт: {{ temp.product_details?.name }}</p>
        <p class="desc">{{ temp.description }}</p>
        <div class="financials">
          <span class="cost">Себ: {{ formatCurrency(temp.cost_price) }}</span>
          <span class="sale">Цена: {{ formatCurrency(temp.sale_price) }}</span>
        </div>
      </div>
    </div>

    <!-- Modal for new template -->
    <div class="modal-backdrop" v-if="showModal" @click.self="showModal = false">
      <div class="modal-content-container standard v-if-anim">
        <div class="modal-header">
          <h2>{{ editMode ? 'Редактировать шаблон' : 'Новый шаблон' }}</h2>
          <button class="close-btn" @click="closeModal">✕</button>
        </div>
        <form @submit.prevent="submitTemplate">
          <div class="form-group">
            <label>Название шаблона</label>
            <input type="text" v-model="formData.name" required />
          </div>
          <div class="form-group">
            <label>Продукт</label>
            <select v-model="formData.product" required>
              <option value="" disabled>Выберите продукт</option>
              <option v-for="p in productsStore.products" :key="p.id" :value="p.id">{{ p.name }}</option>
            </select>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label>Себестоимость</label>
              <input type="number" v-model="formData.cost_price" step="0.01" required />
            </div>
            <div class="form-group">
              <label>Цена продажи</label>
              <input type="number" v-model="formData.sale_price" step="0.01" required />
            </div>
          </div>

          <div class="form-group">
            <label>Описание / Параметры</label>
            <textarea v-model="formData.description" rows="3"></textarea>
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
import { useProductsStore } from '../stores/products'

const productsStore = useProductsStore()
const showModal = ref(false)
const editMode = ref(false)
const editingId = ref(null)

const formData = ref({
  name: '',
  product: '',
  description: '',
  cost_price: '',
  sale_price: ''
})

onMounted(async () => {
  await productsStore.fetchTemplates()
  if(productsStore.products.length === 0) await productsStore.fetchProducts()
})

const formatCurrency = (val) => {
  return Number(val).toLocaleString('ru-RU') + ' ₸'
}

const closeModal = () => {
  showModal.value = false
  editMode.value = false
  editingId.value = null
  formData.value = { name: '', product: '', description: '', cost_price: '', sale_price: '' }
}

const handleEdit = (temp) => {
  editMode.value = true
  editingId.value = temp.id
  formData.value = {
    name: temp.name,
    product: temp.product_details?.id || temp.product,
    description: temp.description || '',
    cost_price: temp.cost_price,
    sale_price: temp.sale_price
  }
  showModal.value = true
}

const submitTemplate = async () => {
  try {
    if (editMode.value) {
      await productsStore.updateTemplate(editingId.value, formData.value)
    } else {
      await productsStore.createTemplate(formData.value)
    }
    closeModal()
  } catch(e) {
    alert('Ошибка при сохранении')
  }
}

const handleDelete = async (id) => {
  if(confirm('Удалить шаблон?')) {
    await productsStore.deleteTemplate(id)
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
.templates-grid { 
  display: grid; 
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); 
  gap: 20px; 
}
.template-card { 
  padding: 20px; 
}
.header { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  margin-bottom: 12px; 
}
.header h3 { 
  margin: 0; 
  font-size: 1.1rem; 
  color: var(--text-main); 
}
.actions {
  display: flex;
  gap: 8px;
}
.btn-edit {
  background: transparent;
  color: var(--text-main);
  border: 1px solid var(--border-color);
  padding: 4px 8px;
  font-size: 0.85rem;
  font-weight: 600;
  transition: all var(--transition-speed) ease;
  border-radius: var(--radius-btn);
}
.btn-edit:hover {
  background: var(--border-color);
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
.product-name { 
  font-weight: 600; 
  margin-bottom: 8px; 
  font-size: 0.95rem;
}
.desc { 
  color: var(--text-muted); 
  font-size: 0.9rem; 
  margin-bottom: 16px; 
  line-height: 1.5;
}
.financials {
  display: flex; 
  justify-content: space-between; 
  font-size: 0.85rem; 
  background: var(--bg-color); 
  padding: 8px 12px; 
  border-radius: var(--radius-btn);
  color: var(--text-muted);
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
.form-actions { 
  display: flex; 
  justify-content: flex-end; 
  gap: 12px; 
  margin-top: 24px;
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
