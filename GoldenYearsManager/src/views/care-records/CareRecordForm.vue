<template>
  <div class="care-record-form">
    <el-form :model="form" label-width="120px" :rules="rules" ref="formRef">
      <el-form-item label="护理内容" prop="care_content">
        <el-select v-model="form.care_type" placeholder="选择护理类型" style="width: 100%">
          <el-option label="日常护理" value="daily" />
          <el-option label="医疗护理" value="medical" />
          <el-option label="康复护理" value="recovery" />
        </el-select>
        <el-input
          v-model="form.care_content"
          type="textarea"
          rows="4"
          placeholder="详细描述护理内容"
          style="margin-top: 10px"
        />
      </el-form-item>

      <el-form-item label="护理日期" prop="care_date">
        <el-date-picker v-model="form.care_date" type="date" value-format="YYYY-MM-DD" />
      </el-form-item>

      <el-form-item label="护理评估" prop="evaluation">
        <el-input
          v-model="form.evaluation"
          type="textarea"
          rows="3"
          placeholder="记录护理效果评估"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitForm">提交</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { createCareRecord, updateCareRecord } from '@/api/care'
import type { FormInstance, FormRules } from 'element-plus'
import type { CareRecordForm } from '@/types'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const formRef = ref<FormInstance>()

const form = ref<CareRecordForm>({
  pid: Number(route.params.pid || route.query.pid),
  caregiver_id: authStore.user?.uid || 0,
  care_type: '',
  care_content: '',
  care_date: new Date().toISOString().split('T')[0],
  evaluation: '',
  plan_id: route.query.planId ? Number(route.query.planId) : undefined,
})

const rules = ref<FormRules>({
  care_content: [
    { required: true, message: '请输入护理内容', trigger: 'blur' },
    { min: 10, message: '护理内容至少10个字符', trigger: 'blur' },
  ],
  care_date: [{ required: true, message: '请选择护理日期', trigger: 'change' }],
  evaluation: [{ min: 5, message: '评估内容至少5个字符', trigger: 'blur' }],
})

const submitForm = async () => {
  try {
    await formRef.value?.validate()
    if (route.params.id) {
      await updateCareRecord(Number(route.params.id), form.value)
    } else {
      await createCareRecord(form.value)
    }
    router.back()
  } catch (error) {
    console.error('提交失败:', error)
  }
}

const resetForm = () => {
  formRef.value?.resetFields()
}
</script>

<style scoped>
.care-record-form {
  padding: 20px;
}
</style>
