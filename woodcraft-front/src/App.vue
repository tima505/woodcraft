<template>
  <div id="app" :class="{ 'layout-dashboard': authStore.isAuthenticated }">
    <AppHeader v-slot="{ collapsed }" v-if="authStore.isAuthenticated" />
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade-slide" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'
import { useThemeStore } from './stores/theme'
import AppHeader from './components/AppHeader.vue'

const authStore = useAuthStore()
const themeStore = useThemeStore()

onMounted(async () => {
  themeStore.initTheme()
  if (authStore.token) {
    await authStore.fetchUser()
  }
})
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

#app.layout-dashboard {
  flex-direction: row;
}

.main-content {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
}

.layout-dashboard .main-content {
  max-width: none;
  margin: 0;
}

/* Page transitions */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
