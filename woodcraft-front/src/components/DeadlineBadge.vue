<template>
  <span 
    v-if="status && status.type !== 'ok'" 
    class="badge deadline-badge" 
    :class="status.type"
  >
    {{ status.label }}
  </span>
</template>

<script setup>
import { computed } from 'vue'
import { getDeadlineStatus } from '../utils/deadline'

const props = defineProps({
  deadline: {
    type: String,
    default: null
  }
})

const status = computed(() => getDeadlineStatus(props.deadline))
</script>

<style scoped>
.deadline-badge {
  display: inline-flex;
  align-items: center;
  font-size: 0.65rem;
  letter-spacing: 0.3px;
  text-transform: uppercase;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 600;
  line-height: 1.4;
}

/* Overdue is vibrant red */
.deadline-badge.overdue {
  background: linear-gradient(135deg, #ff4d4d, #e60000);
  color: #FFFFFF;
  box-shadow: 0 4px 10px rgba(230, 0, 0, 0.2);
  animation: pulse-red 2s infinite;
}

/* Urgent is vibrant orange */
.deadline-badge.urgent {
  background: linear-gradient(135deg, #ffaa00, #ff7700);
  color: #FFFFFF;
  box-shadow: 0 4px 10px rgba(255, 119, 0, 0.2);
}

/* Warning is soft yellow/amber */
.deadline-badge.warning {
  background: linear-gradient(135deg, #ffdd55, #ffbb00);
  color: #333333;
  box-shadow: 0 4px 10px rgba(255, 187, 0, 0.2);
}

@keyframes pulse-red {
  0% { box-shadow: 0 0 0 0 rgba(230, 0, 0, 0.4); }
  70% { box-shadow: 0 0 0 6px rgba(230, 0, 0, 0); }
  100% { box-shadow: 0 0 0 0 rgba(230, 0, 0, 0); }
}
</style>
