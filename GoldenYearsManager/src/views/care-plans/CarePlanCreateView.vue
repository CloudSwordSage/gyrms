<template>
  <div class="care-plan-create">
    <el-card>
      <template #header>
        <h2>新建护理计划</h2>
      </template>

      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="120px"
        @submit.prevent="handleSubmit"
      >
        <el-form-item label="床位号" prop="pid">
          <el-select
            v-model="formData.bedNumber"
            placeholder="请选择床位号"
            filterable
            clearable
            @change="handleBedNumberChange"
          >
            <el-option
              v-for="item in bedNumbers"
              :key="item.bedNumber"
              :label="item.bedNumber"
              :value="item.bedNumber"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="计划名称" prop="plan_name">
          <el-input v-model="formData.planName" />
        </el-form-item>

        <el-form-item label="计划内容" prop="plan_content">
          <el-input v-model="formData.planContent" type="textarea" :rows="5" />
        </el-form-item>

        <el-form-item label="执行频率" prop="frequency">
          <el-select v-model="formData.frequency" placeholder="请选择">
            <el-option label="每日" value="每日" />
            <el-option label="每周" value="每周" />
            <el-option label="每月" value="每月" />
          </el-select>
        </el-form-item>

        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker
            v-model="formData.startDate"
            type="date"
            placeholder="选择日期"
            value-format="YYYY-MM-DD"
            @change="handleStartDateChange"
          />
        </el-form-item>

        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker
            v-model="formData.endDate"
            type="date"
            placeholder="选择日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" native-type="submit">提交</el-button>
          <el-button @click="handleCancel">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { carePlanApi } from '@/api/carePlan'
import { personApi } from '@/api/person'
import type { FormInstance, FormRules } from 'element-plus'

const router = useRouter()
const formRef = ref<FormInstance>()

const formData = ref({
  pid: 0 as number,
  bedNumber: '',
  planName: '',
  planContent: '',
  frequency: '每日',
  startDate: '',
  endDate: '',
  executorId: null,
  executorName: '',
  status: '进行中' as const,
})

const bedNumbers = ref<{ pid: number; bedNumber: string }[]>([])
const bedNumberPage = ref(1)
const bedNumberPageSize = ref(10)
const bedNumberTotal = ref(0)

const loadBedNumbers = async () => {
  try {
    const res = await personApi.getBedNumbers({
      page: bedNumberPage.value,
      page_size: bedNumberPageSize.value,
    })
    bedNumbers.value = res.items
    bedNumberTotal.value = res.total
  } catch (error) {
    console.error('获取床位号失败:', error)
  }
}

const handleBedNumberChange = (bedNumber: string) => {
  const selected = bedNumbers.value.find((item) => item.bedNumber === bedNumber)
  if (selected) {
    formData.value.pid = selected.pid
  }
}

const validateEndDate = (
  rule: unknown,
  value: string,
  callback: (error?: string | Error) => void,
) => {
  if (!value) {
    callback(new Error('请选择结束日期'))
    return
  }
  const startDate = formData.value.startDate
  if (startDate && value < startDate) {
    callback(new Error('结束日期不能早于开始日期'))
  } else {
    callback()
  }
}

const rules = ref<FormRules>({
  pid: [{ required: true, message: '请选择床位号', trigger: 'change' }],
  planName: [{ required: true, message: '请输入计划名称', trigger: 'blur' }],
  planContent: [{ required: true, message: '请输入计划内容', trigger: 'blur' }],
  startDate: [{ required: true, message: '请选择开始日期', trigger: 'change' }],
  endDate: [
    { required: true, message: '请选择结束日期', trigger: 'change' },
    { validator: validateEndDate, trigger: ['change', 'blur'] },
  ],
})

const handleStartDateChange = () => {
  formRef.value?.validateField('endDate')
}

onMounted(() => {
  loadBedNumbers()
})

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    await carePlanApi.createCarePlan(formData.value)
    router.push({ name: 'care-plan-list' })
  } catch (error) {
    console.error('创建护理计划失败:', error)
  }
}

const handleCancel = () => {
  router.go(-1)
}
</script>

<style scoped>
.el-form {
  max-width: 800px;
}
</style>
