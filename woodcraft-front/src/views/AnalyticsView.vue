<template>
  <div>
    <div class="page-header">
      <h2>Сводная аналитика</h2>
    </div>

    <!-- Section 1: Finances -->
    <h3 class="section-title">Финансы (Сегодня)</h3>
    <div class="analytics-grid">
      <div class="stat-card">
        <div class="stat-title">Выручка за сегодня</div>
        <div class="stat-value text-success">{{ metrics.revenue_today || 0 }} ₸</div>
      </div>
      <div class="stat-card">
        <div class="stat-title">Прибыль за сегодня</div>
        <div class="stat-value text-accent">{{ metrics.profit_today || 0 }} ₸</div>
      </div>
      <div class="stat-card">
        <div class="stat-title">Выручка за месяц</div>
        <div class="stat-value">{{ metrics.revenue_month || 0 }} ₸</div>
      </div>
      <div class="stat-card">
        <div class="stat-title">Прибыль за месяц</div>
        <div class="stat-value">{{ metrics.profit_month || 0 }} ₸</div>
      </div>
    </div>

    <!-- Section 2: Production & WIP -->
    <h3 class="section-title">Производство и загрузка</h3>
    <div class="analytics-grid">
      <div class="stat-card">
        <div class="stat-title">Заказы в работе</div>
        <div class="stat-value">{{ metrics.orders_in_progress || 0 }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-title">Новые заказы (ожидают)</div>
        <div class="stat-value">{{ metrics.orders_new || 0 }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-title">Этапов просрочено</div>
        <div class="stat-value text-warning">{{ metrics.overdue_stages_count || 0 }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-title">Самый проблемный этап</div>
        <div class="stat-value text-small">{{ metrics.slowest_stage || '—' }}</div>
      </div>
    </div>

    <div class="charts-and-lists">
      <!-- Section 3: Chart -->
      <div class="chart-section stat-card">
        <h3 class="section-title" style="margin-top: 0;">Выручка за 7 дней</h3>
        <div class="chart-container" v-if="chartData">
          <LineChart :data="chartData" :options="chartOptions" />
        </div>
        <div v-else class="text-muted">Загрузка графика...</div>
      </div>

      <!-- Section 4: Top workers -->
      <div class="workers-section stat-card">
        <h3 class="section-title" style="margin-top: 0;">Топ рабочих (за неделю)</h3>
        <div class="workers-list" v-if="metrics.top_workers && metrics.top_workers.length">
          <div class="worker-row" v-for="(worker, i) in metrics.top_workers" :key="i">
            <span class="worker-rank">#{{ i + 1 }}</span>
            <span class="worker-name">{{ worker.name }}</span>
            <span class="worker-score">{{ worker.stages_done }} этапов</span>
          </div>
        </div>
        <div v-else class="text-muted">Нет данных о работе</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../utils/api'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Line as LineChart } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

const metrics = ref({})
const chartData = ref(null)

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
}

onMounted(async () => {
  try {
    const res = await api.get('/analytics/')
    metrics.value = res.data

    if (res.data.trend_data) {
      chartData.value = {
        labels: res.data.trend_data.map(d => d.date),
        datasets: [
          {
            label: 'Выручка (₸)',
            backgroundColor: '#4f46e5',
            borderColor: '#4f46e5',
            data: res.data.trend_data.map(d => d.revenue)
          }
        ]
      }
    }
  } catch (err) {
    console.error('Failed to load analytics', err)
  }
})
</script>

<style scoped>
.section-title {
  margin-top: 30px;
  margin-bottom: 15px;
  font-size: 1.1rem;
  color: var(--text-main);
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 8px;
}
.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 10px;
}
.stat-card {
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-card);
  padding: 24px;
  display: flex;
  flex-direction: column;
  transition: transform var(--transition-speed) ease;
}
.stat-card:hover {
  transform: translateY(-2px);
  border-color: var(--text-muted);
}
.stat-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-muted);
  margin-bottom: 8px;
}
.stat-value {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-main);
}
.stat-value.text-small {
  font-size: 1.2rem;
  word-break: break-word;
}
.text-success {
  color: #22c55e !important;
}
.text-accent {
  color: var(--accent-color) !important;
}
.text-warning {
  color: var(--color-overdue) !important;
}

.charts-and-lists {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-top: 30px;
}
.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
}
.workers-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.worker-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid var(--border-color);
}
.worker-row:last-child {
  border-bottom: none;
}
.worker-rank {
  font-weight: bold;
  color: var(--accent-color);
  width: 30px;
}
.worker-name {
  flex: 1;
  font-weight: 500;
}
.worker-score {
  font-size: 0.9rem;
  color: var(--text-muted);
}

@media (max-width: 768px) {
  .charts-and-lists {
    grid-template-columns: 1fr;
  }
}
</style>
