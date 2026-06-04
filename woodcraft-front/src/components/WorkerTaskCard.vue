<template>
  <div class="card task-card" :class="{'overdue-card': hasOverdueTask}">
    <div class="card-header" @click="isExpanded = !isExpanded" role="button">
      <div class="header-info">
        <span class="client">Клиент: <strong class="hl">{{ group.clientName }}</strong></span>
        <span class="order-id">Заказ #{{ group.orderNumber }} · {{ group.productName }} · {{ group.tasks.length }} {{ taskWord }}</span>
      </div>
      <div class="header-right">
        <span class="task-count-badge">{{ group.tasks.length }}</span>
        <button class="btn-toggle-expand" :class="{ 'rotated': isExpanded }" tabindex="-1">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
        </button>
      </div>
    </div>
    
    <div class="card-body" :class="{ 'expanded': isExpanded }">
      <div class="card-body-content">
        <div 
          v-for="task in group.tasks" 
          :key="task.id" 
          class="task-item"
          :class="{'task-item-overdue': isTaskOverdue(task), 'task-item-issue': task.status === 'issue'}"
        >
          <div class="task-item-header">
            <div class="task-item-left">
              <span class="stage-badge">{{ task.stage.name }}</span>
              <span class="item-num">Единица {{ task.item_number }}</span>
            </div>
            <div class="task-item-status" v-if="isTaskOverdue(task)">
              <span class="overdue-tag">ПРОСРОЧЕН</span>
            </div>
          </div>

          <div class="deadline-wrap" v-if="task.deadline">
            <span class="deadline-date">Крайний срок: {{ formatDate(task.deadline) }}</span>
            <DeadlineBadge :deadline="task.deadline" />
          </div>
          <div class="deadline-wrap" v-else>
            <span class="deadline-date none">Без дедлайна</span>
          </div>

          <div v-if="task.status === 'issue'" class="issue-banner">
            <div class="issue-header">
              <span class="issue-title">⚠ Возврат на исправление</span>
              <span class="issue-date" v-if="task.returned_at">{{ formatDate(task.returned_at) }}</span>
            </div>
            <div class="issue-from" v-if="task.returned_by_name">
              Вернул: <strong>{{ task.returned_by_name }}</strong>
            </div>
            <div class="issue-note" v-if="task.note">Причина: {{ task.note }}</div>
          </div>

          <div class="actions">
            <button class="btn-primary btn-done" @click.stop="handleComplete(task.id)">Выполнить этап</button>
            <button class="btn-return" @click.stop="handleReturn(task.id)">Вернуть назад</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import DeadlineBadge from './DeadlineBadge.vue'
import { getDeadlineStatus } from '../utils/deadline'

const isExpanded = ref(false)

const props = defineProps({
  group: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['complete', 'return'])

const taskWord = computed(() => {
  const n = props.group.tasks.length
  if (n === 1) return 'задача'
  if (n >= 2 && n <= 4) return 'задачи'
  return 'задач'
})

const isTaskOverdue = (task) => {
  if (!task.deadline) return false
  const status = getDeadlineStatus(task.deadline)
  return status.type === 'overdue'
}

const hasOverdueTask = computed(() => {
  return props.group.tasks.some(t => isTaskOverdue(t))
})

const handleComplete = (taskId) => {
  if(confirm('Подтвердить выполнение этапа?')) {
    emit('complete', taskId)
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleString('ru-RU', { 
    day: 'numeric', 
    month: 'short', 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

const handleReturn = (taskId) => {
  const reason = prompt('Укажите причину возврата на предыдущий этап:')
  if(reason) {
    emit('return', { id: taskId, note: reason })
  }
}
</script>

<style scoped>
.task-card {
  margin-bottom: 20px;
}
.overdue-card {
  border: 2px solid var(--color-overdue);
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--text-muted);
  font-size: 0.9rem;
  padding-bottom: 0;
  cursor: pointer;
  user-select: none;
}
.header-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}
.task-count-badge {
  background: var(--accent-color);
  color: var(--card-bg);
  font-size: 0.75rem;
  font-weight: 700;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.btn-toggle-expand {
  background: transparent;
  border: none;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  transition: transform 0.3s ease, background-color 0.2s ease;
  pointer-events: none;
}
.card-header:hover .btn-toggle-expand {
  background-color: var(--bg-color);
  color: var(--text-main);
}
.btn-toggle-expand.rotated {
  transform: rotate(180deg);
}
.client .hl {
  color: var(--text-main);
}
.order-id {
  font-weight: 600;
  color: var(--text-muted);
  font-size: 0.85rem;
}
.card-body {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.card-body.expanded {
  grid-template-rows: 1fr;
}
.card-body-content {
  overflow: hidden;
}

/* Individual task items inside the grouped card */
.task-item {
  padding: 16px;
  margin-top: 12px;
  background: var(--bg-color);
  border-radius: var(--radius-btn);
  border: 1px solid var(--border-color);
  transition: border-color 0.2s ease;
}
.task-item:first-child {
  margin-top: 16px;
  border-top: none;
}
.task-item-overdue {
  border-color: var(--color-overdue);
  border-width: 2px;
}
.task-item-issue {
  border-left: 4px solid var(--color-overdue);
}
.task-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.task-item-left {
  display: flex;
  align-items: center;
  gap: 10px;
}
.item-num {
  color: var(--text-muted);
  font-weight: 500;
  font-size: 0.85rem;
}
.stage-badge {
  background: var(--card-bg);
  padding: 4px 10px;
  border-radius: var(--radius-badge);
  font-weight: 600;
  font-size: 0.85rem;
  border: 1px solid var(--border-color);
}
.overdue-tag {
  background: var(--color-overdue);
  color: #fff;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: var(--radius-badge);
  letter-spacing: 0.5px;
}
.deadline-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}
.deadline-date {
  font-size: 0.85rem;
  color: var(--text-main);
  font-weight: 500;
}
.deadline-date.none {
  color: var(--text-muted);
  font-style: italic;
}
.issue-banner {
  background: rgba(226, 75, 74, 0.08);
  color: var(--color-overdue);
  padding: 12px;
  border-radius: var(--radius-btn);
  margin-bottom: 12px;
  font-size: 0.9rem;
  border-left: 3px solid var(--color-overdue);
}
.issue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}
.issue-title {
  font-weight: 700;
}
.issue-date {
  font-size: 0.8rem;
  color: var(--text-muted);
  font-weight: 500;
}
.issue-from {
  font-size: 0.85rem;
  color: var(--text-main);
  margin-bottom: 4px;
}
.issue-note {
  font-weight: 400;
  font-size: 0.85rem;
  margin-top: 5px;
  color: var(--text-main);
}
.actions {
  display: flex;
  gap: 10px;
}
.btn-done {
  flex: 2;
}
.btn-return {
  flex: 1;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  border-radius: var(--radius-btn);
  font-size: 0.85rem;
  cursor: pointer;
  transition: all var(--transition-speed) ease;
}
.btn-return:hover {
  background: var(--border-color);
}
</style>
