<template>
  <div class="kanban-board">
    <div class="column" v-for="col in columns" :key="col.id">
      <div class="col-header">
        <h3>{{ col.title }}</h3>
        <span class="count">{{ getOrdersByStatus(col.id).length }}</span>
      </div>
      <div class="col-content">
        <KanbanCard 
          v-for="order in getOrdersByStatus(col.id)" 
          :key="order.id" 
          :order="order" 
          @click="$emit('openOrder', order.id)"
        />
        <div v-if="getOrdersByStatus(col.id).length === 0" class="empty-col">
          Нет заказов
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import KanbanCard from './KanbanCard.vue'

const props = defineProps({
  orders: {
    type: Array,
    required: true
  }
})

defineEmits(['openOrder'])

const columns = [
  { id: 'new', title: 'Новые' },
  { id: 'in_progress', title: 'В работе' },
  { id: 'done', title: 'Готовые' },
  { id: 'defect', title: 'Брак' }
]

const getOrdersByStatus = (status) => {
  return props.orders.filter(o => o.status === status)
}
</script>

<style scoped>
.kanban-board {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  padding-bottom: 20px;
  height: calc(100vh - 150px);
}
.column {
  flex: 1;
  min-width: 300px;
  background-color: var(--card-bg);
  border-radius: var(--radius-card);
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border-color);
}
.col-header {
  padding: 15px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.col-header h3 {
  margin: 0;
  font-size: 1.1rem;
}
.count {
  background: var(--bg-color);
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-muted);
}
.col-content {
  padding: 15px;
  flex: 1;
  overflow-y: auto;
  background-color: var(--bg-color);
  border-radius: 0 0 var(--radius-card) var(--radius-card);
}
.empty-col {
  text-align: center;
  color: var(--text-muted);
  font-size: 0.9rem;
  padding: 20px;
}
</style>
