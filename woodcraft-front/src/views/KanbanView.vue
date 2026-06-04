<template>
  <div>
    <div class="page-header">
      <h2>Канбан доска</h2>
      <button class="btn-primary" @click="showNewOrderModal = true">+ Новый заказ</button>
    </div>

    <KanbanBoard :orders="ordersStore.orders" @openOrder="openOrder" />

    <NewOrderModal 
      v-if="showNewOrderModal" 
      @close="showNewOrderModal = false" 
      @created="handleOrderCreated"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import KanbanBoard from '../components/KanbanBoard.vue'
import NewOrderModal from '../components/NewOrderModal.vue'
import { useOrdersStore } from '../stores/orders'

const ordersStore = useOrdersStore()
const router = useRouter()
const showNewOrderModal = ref(false)

onMounted(async () => {
  await ordersStore.fetchOrders()
})

const openOrder = (id) => {
  router.push({ name: 'order-detail', params: { id } })
}

const handleOrderCreated = () => {
  showNewOrderModal.value = false
  ordersStore.fetchOrders()
}
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>
