<template>
  <div class="card kanban-card" :class="{'overdue-card': isOverdue}" @click="$emit('click')">
    <div v-if="isOverdue" class="overdue-banner">ПРОСРОЧКА</div>
    
    <div class="card-header">
      <span class="order-id">#{{ order.id }}</span>
      <span class="client">{{ order.client_name }}</span>
    </div>
    
    <div class="product-info">
      <strong>{{ order.product_details?.name }}</strong>
      <span class="qty">x{{ order.quantity }}</span>
    </div>
    
    <div class="financials">
      <span class="cost">Себ: {{ formatCurrency(order.cost_price) }}</span>
      <span class="sale">Цена: {{ formatCurrency(order.sale_price) }}</span>
    </div>

    <!-- Find active stage for deadline -->
    <div v-if="activeDeadline" class="deadline-wrapper">
      <DeadlineBadge :deadline="activeDeadline" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import DeadlineBadge from './DeadlineBadge.vue'
import { getDeadlineStatus } from '../utils/deadline'

const props = defineProps({
  order: {
    type: Object,
    required: true
  }
})

defineEmits(['click'])

const activeDeadline = computed(() => {
  if (!props.order.items) return null
  for (const item of props.order.items) {
    if (!item.stages) continue
    for (const stage of item.stages) {
      if (stage.status === 'active' && stage.deadline) {
        return stage.deadline
      }
    }
  }
  return null
})

const isOverdue = computed(() => {
  if (!activeDeadline.value) return false
  const status = getDeadlineStatus(activeDeadline.value)
  return status.type === 'overdue'
})

const formatCurrency = (val) => {
  return Number(val).toLocaleString('ru-RU') + ' ₸'
}
</script>

<style scoped>
.kanban-card {
  margin-bottom: 15px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.kanban-card {
  margin-bottom: 15px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.overdue-card {
  border-left: 4px solid var(--color-overdue);
}
.overdue-banner {
  background-color: var(--color-overdue);
  color: #FFF;
  font-size: 0.7rem;
  font-weight: 700;
  text-align: center;
  padding: 5px 0;
  margin: -20px -20px 12px -20px;
  letter-spacing: 1px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.9rem;
  color: var(--text-muted);
}
.order-id {
  font-weight: 600;
  color: var(--text-main);
}
.product-info {
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
}
.qty {
  font-weight: 600;
  color: var(--text-main);
}
.financials {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: var(--text-muted);
  background: var(--bg-color);
  padding: 6px;
  border-radius: var(--radius-btn);
  margin-bottom: 8px;
}
</style>
