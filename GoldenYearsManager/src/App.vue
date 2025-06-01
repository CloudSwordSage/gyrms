<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import logo from '@/assets/logo.png'

const authStore = useAuthStore()
const router = useRouter()

const isAdmin = computed(() => authStore.hasRole('管理员'))

const logout = async () => {
  await authStore.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="app-layout">
    <header class="app-header">
      <div class="container">
        <div class="header-content">
          <div class="logo">
            <img :src="logo" alt="Golden Years Manager" />
            <h1>Golden Years</h1>
          </div>

          <nav class="main-nav">
            <router-link v-if="authStore.token" to="/person">人员管理</router-link>
            <router-link v-if="authStore.token" to="/care-plans">护理计划</router-link>
            <router-link v-if="authStore.token && isAdmin" to="/user">用户管理</router-link>
            <router-link v-if="authStore.token" to="/profile">个人主页</router-link>
          </nav>

          <div v-if="authStore.token" class="user-info">
            <span>{{ authStore.user?.real_name }}</span>
            <button @click="logout">登出</button>
          </div>
          <router-link v-else to="/login" class="login-btn">登录</router-link>
        </div>
      </div>
    </header>

    <main class="app-main">
      <div class="container">
        <RouterView />
      </div>
    </main>

    <footer class="app-footer">
      <div class="container">
        <p>© 2025 Golden Years Manager - 养老院管理系统</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 0;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo img {
  height: 40px;
}

.logo h1 {
  font-size: 1.5rem;
  margin: 0;
}

.main-nav {
  display: flex;
  gap: 1.5rem;
  flex-grow: 1;
  justify-content: center;
}

.main-nav a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.main-nav a:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.main-nav a.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info button {
  padding: 0.5rem 1rem;
}

.login-btn {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  background-color: #41b883;
}

.app-main {
  flex: 1;
  padding: 2rem 0;
  background-color: #f5f5f5;
}

.app-footer {
  background-color: #1a252f;
  color: white;
  padding: 1rem 0;
  text-align: center;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }

  .main-nav {
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    width: 100%;
  }
}
</style>
