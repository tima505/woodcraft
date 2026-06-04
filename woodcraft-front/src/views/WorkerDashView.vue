<template>
  <div class="dashboard">
    <div 
      v-if="urgentOrOverdueTasks.length > 0" 
      class="alert-banner card" 
      :class="{ 'has-overdue': hasOverdue }"
    >
      <strong>Внимание!</strong> У вас есть срочные или требующие внимания задачи ({{ urgentOrOverdueTasks.length }} шт).
    </div>

    <div class="dash-header">
      <h2>Мои задачи</h2>
      <div class="my-stages">
        <span class="stage-tag" v-for="st in authStore.user?.stages" :key="st.id">{{ st.name }}</span>
      </div>
    </div>

    <div class="tasks-grid">
      <WorkerTaskCard 
        v-for="group in groupedTasks" 
        :key="group.orderNumber" 
        :group="group" 
        @complete="completeTask"
        @return="returnTask"
      />
      <div v-if="ordersStore.dashboardTasks.length === 0" class="empty-state">
        Нет активных задач
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useOrdersStore } from '../stores/orders'
import WorkerTaskCard from '../components/WorkerTaskCard.vue'
import { getDeadlineStatus } from '../utils/deadline'

const authStore = useAuthStore()
const ordersStore = useOrdersStore()

let intervalId = null

const loadTasks = async () => {
  await ordersStore.fetchDashboardTasks()
}

onMounted(() => {
  loadTasks()
  // Refresh every minute
  intervalId = setInterval(loadTasks, 60000)
})

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
})

const groupedTasks = computed(() => {
  const map = {}
  for (const task of ordersStore.dashboardTasks) {
    const key = task.order_number
    if (!map[key]) {
      map[key] = {
        orderNumber: key,
        clientName: task.client_name,
        productName: task.product_name,
        tasks: []
      }
    }
    map[key].tasks.push(task)
  }
  return Object.values(map)
})

const urgentOrOverdueTasks = computed(() => {
  return ordersStore.dashboardTasks.filter(t => {
    if (!t.deadline) return false
    const status = getDeadlineStatus(t.deadline)
    return status.type === 'overdue' || status.type === 'urgent' || status.type === 'warning'
  })
})

const hasOverdue = computed(() => {
  return ordersStore.dashboardTasks.some(t => {
    if (!t.deadline) return false
    const status = getDeadlineStatus(t.deadline)
    return status.type === 'overdue'
  })
})

const completeTask = async (id) => {
  await ordersStore.completeStage(id)
}

const returnTask = async ({id, note}) => {
  await ordersStore.returnStage(id, note)
}
</script>

<style scoped>
.dashboard {
  max-width: 800px;
  margin: 0 auto;
}
.alert-banner {
  background: var(--bg-color);
  color: var(--text-main);
  border: 1px solid var(--border-color);
  margin-bottom: 24px;
}
.alert-banner.has-overdue {
  border-left: 4px solid var(--color-overdue);
  color: var(--color-overdue);
}
.dash-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.my-stages {
  display: flex;
  gap: 10px;
}
.stage-tag {
  background: var(--bg-color);
  padding: 4px 10px;
  border-radius: var(--radius-badge);
  font-size: 0.8rem;
  font-weight: 600;
  border: 1px solid var(--border-color);
}
.empty-state {
  text-align: center;
  color: var(--text-muted);
  padding: 40px;
  background: var(--card-bg);
  border-radius: var(--radius-card);
  border: 1px solid var(--border-color);
}
</style>
