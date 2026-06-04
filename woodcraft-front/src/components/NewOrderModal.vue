<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal-content-container standard v-if-anim">
      <div class="modal-header">
        <h2>Новый заказ</h2>
        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>

      <div class="tabs">
        <button :class="{active: activeTab === 'template'}" @click="activeTab = 'template'">Из шаблона</button>
        <button :class="{active: activeTab === 'custom'}" @click="activeTab = 'custom'">Уникальный</button>
      </div>

      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label>Клиент *</label>
          <input type="text" v-model="clientName" required />
        </div>

        <!-- Product lines -->
        <div class="product-lines">
          <div 
            v-for="(line, idx) in productLines" 
            :key="idx" 
            class="product-line"
          >
            <div class="product-line-header">
              <span class="product-line-num">Продукт {{ idx + 1 }}</span>
              <button 
                v-if="productLines.length > 1" 
                type="button" 
                class="btn-remove-line" 
                @click="removeLine(idx)"
                title="Удалить"
              >✕</button>
            </div>

            <div v-if="activeTab === 'template'" class="form-group">
              <label>Шаблон *</label>
              <select v-model="line.selectedTemplateId" @change="applyTemplate(idx)" required>
                <option value="" disabled>Выберите шаблон</option>
                <option v-for="t in productsStore.templates" :key="t.id" :value="t.id">{{ t.name }}</option>
              </select>
            </div>

            <div v-if="activeTab === 'custom'" class="form-group">
              <label>Продукт *</label>
              <select v-model="line.product" required>
                <option value="" disabled>Выберите продукт</option>
                <option v-for="p in productsStore.products" :key="p.id" :value="p.id">{{ p.name }}</option>
              </select>
            </div>

            <div class="form-group">
              <label>Количество *</label>
              <input type="number" v-model="line.quantity" min="1" required />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Себестоимость (₸) *</label>
                <input type="number" v-model="line.cost_price" step="0.01" required />
              </div>
              <div class="form-group">
                <label>Цена продажи (₸) *</label>
                <input type="number" v-model="line.sale_price" step="0.01" required />
              </div>
            </div>

            <div class="form-group">
              <label>Описание</label>
              <textarea v-model="line.description" rows="2"></textarea>
            </div>

            <div v-if="getProductObj(line) && getProductObj(line).stages.length" class="order-stages-config">
              <h4>Дедлайны этапов</h4>
              <p class="section-desc">Укажите крайние сроки для этапов (необязательно)</p>
              <div class="stage-deadline-list">
                <div class="stage-deadline-item" v-for="stage in getProductObj(line).stages" :key="stage.id">
                  <span class="stage-name">{{ stage.name }}</span>
                  <input type="datetime-local" class="deadline-input" v-model="line.stageDeadlines[stage.id]" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <button type="button" class="btn-add-line" @click="addLine">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
          Добавить ещё продукт
        </button>

        <div class="form-actions">
          <button type="button" @click="$emit('close')" class="btn-cancel">Отмена</button>
          <button type="submit" class="btn-primary" :disabled="isSubmitting">
            {{ isSubmitting ? 'Создание...' : `Создать ${productLines.length > 1 ? productLines.length + ' заказа' : 'заказ'}` }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useOrdersStore } from '../stores/orders'
import { useProductsStore } from '../stores/products'

const emit = defineEmits(['close', 'created'])

const ordersStore = useOrdersStore()
const productsStore = useProductsStore()

const activeTab = ref('template')
const isSubmitting = ref(false)
const clientName = ref('')

const createEmptyLine = () => ({
  selectedTemplateId: '',
  product: '',
  quantity: 1,
  cost_price: '',
  sale_price: '',
  description: '',
  stageDeadlines: {}
})

const productLines = ref([createEmptyLine()])

onMounted(async () => {
  if (productsStore.products.length === 0) await productsStore.fetchProducts()
  if (productsStore.templates.length === 0) await productsStore.fetchTemplates()
})

const addLine = () => {
  productLines.value.push(createEmptyLine())
}

const removeLine = (idx) => {
  productLines.value.splice(idx, 1)
}

const applyTemplate = (idx) => {
  const line = productLines.value[idx]
  const t = productsStore.templates.find(x => x.id === line.selectedTemplateId)
  if (t) {
    line.product = t.product
    line.cost_price = t.cost_price
    line.sale_price = t.sale_price
    line.description = t.description
  }
}

const getProductObj = (line) => {
  if (!line.product) return null
  return productsStore.products.find(p => p.id === line.product)
}

const submitForm = async () => {
  isSubmitting.value = true
  try {
    for (const line of productLines.value) {
      const payload = {
        client_name: clientName.value,
        product: line.product,
        quantity: line.quantity,
        cost_price: line.cost_price,
        sale_price: line.sale_price,
        description: line.description,
        stage_deadlines: line.stageDeadlines
      }
      await ordersStore.createOrder(payload)
    }
    emit('created')
  } catch (err) {
    alert('Ошибка при создании заказа')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.modal-content-container.standard {
  max-width: 540px;
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
.tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
}
.tabs button {
  flex: 1;
  padding: 10px;
  background: var(--bg-color);
  color: var(--text-muted);
  border: 1px solid var(--border-color);
  font-size: 0.9rem;
  font-weight: 500;
  transition: all var(--transition-speed) ease;
}
.tabs button.active {
  background: var(--accent-color);
  color: var(--card-bg);
  border-color: var(--accent-color);
}
.form-group {
  margin-bottom: 16px;
}
.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-main);
}
.form-row {
  display: flex;
  gap: 15px;
}
.form-row .form-group {
  flex: 1;
}

/* Product lines */
.product-lines {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.product-line {
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-card);
  padding: 20px;
  transition: border-color 0.2s ease;
}
.product-line:hover {
  border-color: var(--accent-color);
}
.product-line-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.product-line-num {
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--text-main);
}
.btn-remove-line {
  background: none;
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-remove-line:hover {
  background: var(--color-overdue);
  color: #fff;
  border-color: var(--color-overdue);
}
.btn-add-line {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 12px;
  margin-top: 16px;
  background: transparent;
  border: 2px dashed var(--border-color);
  color: var(--text-muted);
  font-size: 0.9rem;
  font-weight: 600;
  border-radius: var(--radius-btn);
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-add-line:hover {
  border-color: var(--accent-color);
  color: var(--accent-color);
  background: rgba(0,0,0,0.02);
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
.order-stages-config {
  background: var(--card-bg);
  padding: 16px;
  border-radius: var(--radius-btn);
  margin-top: 12px;
  border: 1px solid var(--border-color);
}
.order-stages-config h4 {
  margin-bottom: 4px;
  font-size: 0.95rem;
}
.section-desc {
  color: var(--text-muted);
  font-size: 0.8rem;
  margin-bottom: 16px;
}
.stage-deadline-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.stage-deadline-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  padding: 10px 14px;
  border-radius: var(--radius-btn);
}
.stage-deadline-item .stage-name {
  font-weight: 500;
  font-size: 0.9rem;
}
.deadline-input {
  max-width: 200px;
  padding: 6px 10px;
  font-size: 0.85rem;
}
</style>
