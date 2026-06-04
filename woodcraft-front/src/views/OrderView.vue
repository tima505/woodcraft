<template>
  <div class="order-page" v-if="order">
    <div class="page-header">
      <div class="header-left">
        <button class="btn-back" @click="router.push('/kanban')">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
          Назад
        </button>
        <h2>Заказ #{{ order.id }} — {{ order.client_name }}</h2>
      </div>
      <div class="header-actions" v-if="order.status !== 'done' && order.status !== 'defect'">
        <button class="btn-defect" @click="markDefect">В брак</button>
        <button class="btn-primary" @click="markDone">Отметить готовым</button>
      </div>
    </div>

    <div class="order-info card">
      <p><strong>Продукт:</strong> {{ order.product_details?.name }} (x{{ order.quantity }})</p>
      <p><strong>Описание:</strong> {{ order.description || 'Нет' }}</p>
      <p>
        <strong>Финансы:</strong> Себестоимость {{ formatCurrency(order.cost_price) }}, 
        Цена {{ formatCurrency(order.sale_price) }} 
        <span class="margin-badge">Маржа: {{ calcMargin }}%</span>
      </p>
    </div>

    <div class="mini-kanban-board">
      <div class="mini-kanban-column" v-for="col in kanbanColumns" :key="col.name">
        <div class="column-header">
          <h3>{{ col.name }}</h3>
          <span class="count-badge">{{ col.units.length }}</span>
        </div>
        <div class="column-cards">
          <div class="unit-card" v-for="unit in col.units" :key="unit.id" :class="{'overdue-border': unit.isOverdue}">
            <h4>Единица {{ unit.number }}</h4>
            
            <template v-if="unit.currentStage">
              <div class="stage-status">
                <span class="status-badge" :class="unit.isOverdue ? 'status-overdue' : 'status-' + unit.currentStage.status">
                  {{ unit.isOverdue ? 'ПРОСРОЧЕН' : statusLabels[unit.currentStage.status] }}
                </span>
                <DeadlineBadge :deadline="unit.currentStage.deadline" v-if="unit.currentStage.status === 'active' || unit.currentStage.status === 'issue'" />
              </div>
              <div class="stage-worker" v-if="unit.currentStage.assigned_worker">
                Рабочий: {{ unit.currentStage.assigned_worker.user?.first_name || '—' }}
              </div>
              <div v-if="unit.currentStage.note" class="stage-note">Примечание: {{ unit.currentStage.note }}</div>
            </template>
            <template v-else>
              <span class="status-badge status-done" style="display: inline-block; margin-top: 10px;">Все этапы завершены</span>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useOrdersStore } from '../stores/orders'
import api from '../utils/api'
import DeadlineBadge from '../components/DeadlineBadge.vue'

const route = useRoute()
const router = useRouter()
const ordersStore = useOrdersStore()
const order = ref(null)

const statusLabels = {
  pending: 'Ожидает',
  active: 'В работе',
  done: 'Готово',
  issue: 'Проблема'
}

onMounted(async () => {
  const orderId = route.params.id
  order.value = await ordersStore.getOrder(orderId)
})

const calcMargin = computed(() => {
  if (!order.value || !order.value.sale_price || !order.value.cost_price) return 0
  const margin = ((order.value.sale_price - order.value.cost_price) / order.value.sale_price) * 100
  return margin.toFixed(1)
})

const formatCurrency = (val) => {
  return Number(val).toLocaleString('ru-RU') + ' ₸'
}

const isOverdue = (st) => {
  if (!st || st.status !== 'active') return false
  if (!st.deadline) return false
  return new Date(st.deadline) < new Date()
}

const kanbanColumns = computed(() => {
  if (!order.value || !order.value.items || order.value.items.length === 0) return []

  const firstItem = order.value.items[0]
  const stagesOrdered = [...firstItem.stages].sort((a, b) => a.stage.order - b.stage.order)
  
  const columns = stagesOrdered.map(st => ({
    name: st.stage.name,
    order: st.stage.order,
    units: []
  }))
  columns.push({ name: 'Завершено', order: 9999, units: [] })

  order.value.items.forEach(item => {
    const sortedItemStages = [...item.stages].sort((a, b) => a.stage.order - b.stage.order)
    const currentStage = sortedItemStages.find(s => s.status !== 'done')

    const unitData = {
      ...item,
      currentStage: currentStage || null,
      isOverdue: currentStage ? isOverdue(currentStage) : false
    }

    if (currentStage) {
      const col = columns.find(c => c.name === currentStage.stage.name)
      if (col) col.units.push(unitData)
    } else {
      const lastCol = columns[columns.length - 1]
      lastCol.units.push(unitData)
    }
  })

  return columns
})

const markDefect = async () => {
  if(confirm('Переместить заказ в брак?')) {
    await api.patch(`orders/${order.value.id}/`, { status: 'defect' })
    router.push('/kanban')
  }
}

const markDone = async () => {
  if(confirm('Отметить заказ как полностью готовый?')) {
    await api.patch(`orders/${order.value.id}/`, { status: 'done' })
    router.push('/kanban')
  }
}
</script>

<style scoped>
.order-page {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 120px); /* Fill remaining space minus header/padding */
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-shrink: 0;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}
.header-left h2 {
  margin: 0;
  font-size: 1.5rem;
}
.btn-back {
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  border-radius: var(--radius-btn);
  padding: 8px 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-back:hover {
  background: var(--bg-color);
  border-color: var(--text-muted);
}
.header-actions {
  display: flex;
  gap: 12px;
}
.order-info {
  padding: 20px;
  margin-bottom: 24px;
  line-height: 1.6;
  flex-shrink: 0;
}
.margin-badge {
  background: var(--accent-color);
  color: var(--card-bg);
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-left: 10px;
}

/* KANBAN STYLES */
.mini-kanban-board {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  overflow-y: hidden;
  flex: 1;
  padding-bottom: 10px;
}
.mini-kanban-column {
  min-width: 280px;
  width: 280px;
  background: var(--bg-color);
  border-radius: var(--radius-card);
  padding: 15px;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border-color);
  max-height: 100%;
}
.column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  flex-shrink: 0;
}
.column-header h3 {
  margin: 0;
  font-size: 1rem;
  color: var(--text-main);
}
.count-badge {
  background: var(--border-color);
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
}
.column-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow-y: auto;
  padding-right: 5px;
}
.unit-card {
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-btn);
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02);
  flex-shrink: 0;
}
.unit-card h4 {
  margin: 0 0 12px 0;
  font-size: 1rem;
  color: var(--text-main);
}
.overdue-border {
  border: 2px solid var(--color-overdue) !important;
}
.stage-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.stage-worker {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-top: 10px;
}
.stage-note {
  color: var(--color-overdue);
  font-size: 0.85rem;
  margin-top: 10px;
  font-weight: 500;
  background: rgba(226, 75, 74, 0.05);
  padding: 8px;
  border-radius: 4px;
  border-left: 3px solid var(--color-overdue);
}

/* BADGES */
.status-badge {
  font-size: 0.75rem;
  padding: 4px 10px;
  border-radius: 4px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.status-pending { 
  background: var(--bg-color); 
  color: var(--text-muted); 
  border: 1px solid var(--border-color);
}
.status-active { 
  background: var(--border-color); 
  color: var(--text-main); 
  border: 1px solid var(--text-muted);
}
.status-done { 
  background: var(--border-color); 
  color: var(--text-muted); 
}
.status-issue { 
  background: rgba(226, 75, 74, 0.1); 
  color: var(--color-overdue); 
  border: 1px solid var(--color-overdue);
}
.status-overdue {
  background: var(--color-overdue);
  color: #fff;
  border: 1px solid var(--color-overdue);
}

.btn-defect {
  background: var(--card-bg);
  color: var(--color-overdue);
  border: 1px solid var(--color-overdue);
  padding: 10px 20px;
  font-size: 0.9rem;
  font-weight: 600;
  border-radius: var(--radius-btn);
  transition: all var(--transition-speed) ease;
  cursor: pointer;
}
.btn-defect:hover {
  background: var(--color-overdue);
  color: #FFFFFF;
}
</style>
