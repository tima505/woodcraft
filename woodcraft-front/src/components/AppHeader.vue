<template>
  <aside class="sidebar">
    <div class="sidebar-top">
      <div class="logo">
        <div class="logo-icon"></div>
        <h1>ДРЕВОПРО</h1>
      </div>
      <nav class="nav">
        <!-- Admin Links -->
        <template v-if="authStore.isAdmin">
          <router-link to="/kanban" class="nav-item">
            <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="9" y1="3" x2="9" y2="21"></line><line x1="15" y1="3" x2="15" y2="21"></line><line x1="12" y1="8" x2="12" y2="8.01"></line><line x1="12" y1="12" x2="12" y2="12.01"></line></svg>
            <span>Канбан</span>
          </router-link>
          <router-link to="/products" class="nav-item">
            <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
            <span>Продукты</span>
          </router-link>
          <router-link to="/workers" class="nav-item">
            <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
            <span>Рабочие</span>
          </router-link>
          <router-link to="/analytics" class="nav-item">
            <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
            <span>Аналитика</span>
          </router-link>
          <router-link to="/templates" class="nav-item">
            <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>
            <span>Шаблоны</span>
          </router-link>
          <router-link to="/settings" class="nav-item">
            <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
            <span>Настройки</span>
          </router-link>
        </template>
        <!-- Worker Links -->
        <template v-else>
          <router-link to="/dashboard" class="nav-item">
            <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="9"></rect><rect x="14" y="3" width="7" height="5"></rect><rect x="14" y="12" width="7" height="9"></rect><rect x="3" y="16" width="7" height="5"></rect></svg>
            <span>Мои задачи</span>
          </router-link>
        </template>
      </nav>
    </div>
    <div class="sidebar-bottom">
      <div class="theme-switch-container">
        <span class="theme-label">Темная тема</span>
        <button @click="themeStore.toggleTheme" class="theme-toggle-btn" aria-label="Toggle Theme">
          <svg v-if="themeStore.isDark" class="theme-icon sun" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
          <svg v-else class="theme-icon moon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
        </button>
      </div>
      <div class="user-profile">
        <div class="user-avatar">
          {{ (authStore.user?.first_name || authStore.user?.username || 'U')[0].toUpperCase() }}
        </div>
        <div class="user-info">
          <span class="user-name">{{ authStore.user?.first_name || authStore.user?.username }}</span>
          <span class="user-role">{{ authStore.isAdmin ? 'Администратор' : 'Рабочий' }}</span>
        </div>
      </div>
      <button @click="handleLogout" class="btn-logout-sidebar">
        <svg class="logout-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
        <span>Выйти</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { useThemeStore } from '../stores/theme'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const themeStore = useThemeStore()
const router = useRouter()

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  width: 260px;
  min-width: 260px;
  height: 100vh;
  position: sticky;
  top: 0;
  background-color: var(--card-bg);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 24px 20px;
  transition: background-color var(--transition-speed) ease, border-color var(--transition-speed) ease;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 32px;
  padding-left: 8px;
}

.logo-icon {
  width: 24px;
  height: 24px;
  background-color: var(--accent-color);
  border-radius: 6px;
  position: relative;
}

.logo-icon::after {
  content: '';
  position: absolute;
  top: 4px;
  left: 4px;
  width: 16px;
  height: 16px;
  border: 2px solid var(--card-bg);
  border-radius: 4px;
}

.logo h1 {
  font-size: 1.25rem;
  color: var(--text-main);
  margin: 0;
  letter-spacing: 0.5px;
}

.nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text-muted);
  font-weight: 500;
  font-size: 0.95rem;
  padding: 12px 16px;
  border-radius: var(--radius-btn);
  transition: all var(--transition-speed) cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-item:hover {
  color: var(--text-main);
  background-color: var(--bg-color);
}

.nav-item.router-link-active {
  color: var(--card-bg);
  background-color: var(--accent-color);
}

.nav-icon {
  transition: stroke var(--transition-speed) ease;
}

.nav-item:hover .nav-icon {
  stroke: var(--text-main);
}

.nav-item.router-link-active .nav-icon {
  stroke: var(--card-bg);
}

.sidebar-bottom {
  display: flex;
  flex-direction: column;
  gap: 20px;
  border-top: 1px solid var(--border-color);
  padding-top: 20px;
}

.theme-switch-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 8px;
}

.theme-label {
  font-size: 0.85rem;
  color: var(--text-muted);
  font-weight: 500;
}

.theme-toggle-btn {
  background-color: var(--bg-color);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all var(--transition-speed) ease;
}

.theme-toggle-btn:hover {
  background-color: var(--border-color);
  transform: rotate(15deg);
}

.theme-icon {
  stroke: var(--text-main);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  background-color: var(--bg-color);
  border-radius: var(--radius-btn);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--accent-color);
  color: var(--card-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.95rem;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-main);
}

.user-role {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.btn-logout-sidebar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  width: 100%;
  padding: 10px;
  font-size: 0.9rem;
  transition: all var(--transition-speed) ease;
}

.btn-logout-sidebar:hover {
  background-color: var(--color-overdue);
  color: #FFFFFF;
  border-color: var(--color-overdue);
}

.btn-logout-sidebar:hover .logout-icon {
  stroke: #FFFFFF;
}
</style>
