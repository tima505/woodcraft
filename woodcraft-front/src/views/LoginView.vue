<template>
  <div class="login-container">
    <div class="card login-card">
      <h2 class="title">ДРЕВОПРО</h2>
      <p class="subtitle">Вход в систему</p>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label>Логин</label>
          <input type="text" v-model="username" required placeholder="Введите логин" />
        </div>
        <div class="form-group">
          <label>Пароль</label>
          <input type="password" v-model="password" required placeholder="Введите пароль" />
        </div>
        
        <div v-if="error" class="error-msg">{{ error }}</div>
        
        <button type="submit" class="btn-primary login-btn">Войти</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()
const authStore = useAuthStore()

const handleLogin = async () => {
  try {
    error.value = ''
    await authStore.login(username.value, password.value)
    if (authStore.isAdmin) {
      router.push({ name: 'kanban' })
    } else {
      router.push({ name: 'dashboard' })
    }
  } catch (err) {
    error.value = 'Неверный логин или пароль'
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  margin: -30px;
  background-color: var(--bg-color);
}
.login-card {
  width: 100%;
  max-width: 400px;
  padding: 40px;
}
.title {
  text-align: center;
  margin-bottom: 8px;
  color: var(--text-main);
  font-size: 1.6rem;
  letter-spacing: 1px;
}
.subtitle {
  text-align: center;
  color: var(--text-muted);
  margin-bottom: 30px;
  font-size: 0.9rem;
}
.form-group {
  margin-bottom: 20px;
}
.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  font-size: 0.85rem;
}
.error-msg {
  color: var(--color-overdue);
  margin-bottom: 15px;
  font-size: 0.85rem;
  text-align: center;
  background: rgba(226, 75, 74, 0.1);
  padding: 8px;
  border-radius: 4px;
}
.login-btn {
  width: 100%;
  padding: 12px;
  font-size: 1rem;
}
</style>
