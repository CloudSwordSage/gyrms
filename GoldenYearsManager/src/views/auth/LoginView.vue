<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2>养老院管理系统登录</h2>
      <el-form ref="loginForm" :model="form" :rules="rules" @submit.prevent="handleLogin">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" prefix-icon="User" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading" class="login-btn">
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const form = ref({
  username: '',
  password: '',
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { max: 117, message: '密码长度不能超过117个字符', trigger: 'blur' },
  ],
}

const loading = ref(false)

const handleLogin = async () => {
  try {
    loading.value = true
    await authStore.getPublicKey()
    const success = await authStore.login(form.value.username, form.value.password)
    if (success) {
      console.log('登录成功，跳转到/person')
      router.push('/person').catch((err) => {
        console.error('路由跳转失败:', err)
      })
    } else {
      console.error('登录失败，请检查凭证')
    }
  } catch (error) {
    console.error('登录失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f7fa;
}
.login-card {
  width: 400px;
  padding: 20px;
}
.login-btn {
  width: 100%;
}
</style>
