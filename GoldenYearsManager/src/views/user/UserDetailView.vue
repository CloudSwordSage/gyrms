<template>
  <div class="user-detail">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户详情</span>
          <div>
            <el-button @click="handleBack">返回</el-button>
            <el-button type="primary" @click="handleEdit" v-if="authStore.user?.role === '管理员'">
              编辑
            </el-button>
          </div>
        </div>
      </template>

      <el-descriptions :column="1" border>
        <el-descriptions-item label="用户名">{{ data.username || '-' }}</el-descriptions-item>
        <el-descriptions-item label="姓名">{{ data.realName || '-' }}</el-descriptions-item>
        <el-descriptions-item label="角色">
          <el-tag :type="getRoleTagType(data.role)">
            {{ data.role || '-' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="电话">{{ data.phone || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="data.isActivate ? 'success' : 'danger'">
            {{ data.isActivate ? '激活' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ data.createTime || '-' }}</el-descriptions-item>
        <el-descriptions-item label="最后登录时间">{{
          data.lastLogin || '-'
        }}</el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getUserDetail } from '@/api/user'
import { useAuthStore } from '@/stores/auth'
import type { User } from '@/types'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const data = ref<Partial<User>>({
  uid: 0,
  username: '',
  realName: '',
  role: '护理工',
  phone: '',
  isActivate: true,
})

const fetchData = async () => {
  try {
    const userId = Number(route.params.id)
    if (isNaN(userId)) {
      throw new Error('无效的用户ID')
    }
    const res = await getUserDetail(userId)
    data.value = res.data
  } catch (error) {
    console.error('获取用户详情失败:', error)
    ElMessage.error('获取用户详情失败')
  }
}

const handleEdit = () => {
  router.push(`/user/edit/${route.params.id}`)
}

const handleBack = () => {
  router.push('/user')
}

const getRoleTagType = (role?: string) => {
  switch (role) {
    case '管理员':
      return 'danger'
    case '护理主任':
      return 'warning'
    default:
      return 'success'
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.user-detail {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
