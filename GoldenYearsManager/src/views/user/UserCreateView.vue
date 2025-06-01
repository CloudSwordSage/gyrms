<template>
  <div class="user-create">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>新增用户</span>
        </div>
      </template>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="姓名" prop="realName">
          <el-input v-model="form.realName" placeholder="请输入姓名" />
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
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">提交</el-button>
          <el-button @click="handleBack">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { CreateUser } from '@/types'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { createUser } from '@/api/user'
import type { FormInstance, FormRules } from 'element-plus'

const form = ref<CreateUser>({
  username: '',
  password: '',
  realName: '',
  role: '护理工',
  phone: '',
  isActivate: true,
})

const rules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  realName: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }],
}

const formRef = ref<FormInstance>()
const router = useRouter()

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    const res = await createUser(form.value)
    ElMessage.success('创建成功')
    router.push(`/user/${res.data.uid}`)
  } catch (error) {
    console.error('创建用户失败:', error)
    ElMessage.error('创建失败')
  }
}

const handleBack = () => {
  router.push('/user')
}
</script>

<style scoped>
.user-create {
  padding: 20px;
}
.card-header {
  font-size: 18px;
  font-weight: bold;
}
</style>
