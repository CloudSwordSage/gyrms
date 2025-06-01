<template>
  <div class="profile-container">
    <h1>个人主页</h1>

    <div v-if="user">
      <div v-if="!isEditing">
        <div class="profile-field">
          <label>用户名:</label>
          <span>{{ user.username }}</span>
        </div>
        <div class="profile-field">
          <label>姓名:</label>
          <span>{{ user.realName }}</span>
        </div>
        <div class="profile-field">
          <label>电话:</label>
          <span>{{ user.phone }}</span>
        </div>
        <div class="profile-field">
          <label>角色:</label>
          <span>{{ user.role }}</span>
        </div>
        <button @click="isEditing = true">编辑</button>
        <button @click="handleCare">我的护理记录</button>
      </div>

      <div v-else>
        <div class="profile-field">
          <label>用户名:</label>
          <input v-model="formData.username" disabled />
        </div>
        <div class="profile-field">
          <label>姓名:</label>
          <input v-model="formData.realName" />
        </div>
        <div class="profile-field">
          <label>电话:</label>
          <input v-model="formData.phone" />
        </div>
        <div class="buttons">
          <button @click="handleSave">保存</button>
          <button @click="isEditing = false">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { getUserDetail, updateUser } from '@/api/user'
import type { User } from '@/types'

const router = useRouter()
const authStore = useAuthStore()
const user = ref<User | null>(null)
const isEditing = ref(false)
const formData = ref<Partial<User>>({})

const fetchUser = async () => {
  if (authStore.user?.uid) {
    const { data } = await getUserDetail(authStore.user.uid)
    user.value = data
    formData.value = { ...data }
  }
}

const handleSave = async () => {
  if (authStore.user?.uid && formData.value) {
    await updateUser(authStore.user.uid, formData.value)
    await fetchUser()
    isEditing.value = false
  }
}

onMounted(() => {
  fetchUser()
})

const handleCare = () => {
  router.push('/care-records/profile')
}
</script>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.profile-field {
  margin-bottom: 15px;
}

.profile-field label {
  display: inline-block;
  width: 80px;
  font-weight: bold;
}

.buttons {
  margin-top: 20px;
}

button {
  margin-right: 10px;
  padding: 5px 15px;
}
</style>
