<template>
  <div class="user-edit">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>编辑用户</span>
        </div>
      </template>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" disabled placeholder="用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="留空则不修改密码" />
        </el-form-item>
        <el-form-item label="姓名" prop="real_name">
          <el-input v-model="form.real_name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" placeholder="请选择角色">
            <el-option label="管理员" value="管理员" />
            <el-option label="护理主任" value="护理主任" />
            <el-option label="护理工" value="护理工" />
          </el-select>
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入电话" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.is_activate" active-text="启用" inactive-text="禁用" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">保存</el-button>
          <el-button @click="handleBack">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getUserDetail, updateUser } from '@/api/user'
import type { FormInstance, FormRules } from 'element-plus'

const route = useRoute()
const router = useRouter()
const uid = Number(route.params.id)
console.log(route.params)

const form = ref<{
  username: string
  password: string
  real_name: string
  role: '管理员' | '护理工' | '护理主任'
  phone: string
  is_activate: boolean
}>({
  username: '',
  password: '',
  real_name: '',
  role: '护理工',
  phone: '',
  is_activate: true,
})

const rules: FormRules = {
  real_name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }],
  phone: [{ required: true, message: '请输入电话', trigger: 'blur' }],
}

const formRef = ref<FormInstance>()

onMounted(async () => {
  try {
    const { data: user } = await getUserDetail(uid)
    form.value = {
      username: user.username,
      password: '',
      real_name: user.realName,
      role: user.role as '管理员' | '护理工' | '护理主任',
      phone: user.phone,
      is_activate: user.isActivate ?? true,
    }
  } catch (error) {
    console.error('获取用户详情失败:', error)
    ElMessage.error('获取用户信息失败')
  }
})

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    const data: Partial<{
      username: string
      password?: string
      real_name: string
      role: '管理员' | '护理工' | '护理主任'
      phone: string
      is_activate: boolean
    }> = { ...form.value }
    // 如果密码为空则不更新密码
    if (!data.password) {
      delete data.password
    }
    await updateUser(uid, data)
    ElMessage.success('更新成功')
    router.push(`/user/${uid}`)
  } catch (error) {
    console.error('更新用户失败:', error)
    ElMessage.error('更新失败')
  }
}

const handleBack = () => {
  router.push('/user')
}
</script>

<style scoped>
.user-edit {
  padding: 20px;
}
.card-header {
  font-size: 18px;
  font-weight: bold;
}
</style>
