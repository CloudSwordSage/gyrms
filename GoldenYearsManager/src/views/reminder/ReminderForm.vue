<template>
  <div class="reminder-form">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>{{ formTitle }}</span>
        </div>
      </template>

      <el-form :model="form" label-width="120px" ref="formRef">
        <el-form-item label="提醒类型" prop="reminder_type" required>
          <el-select v-model="form.reminder_type" placeholder="请选择提醒类型">
            <el-option label="用药提醒" value="medication" />
            <el-option label="复诊提醒" value="follow_up" />
            <el-option label="检查提醒" value="examination" />
          </el-select>
        </el-form-item>

        <el-form-item label="周期" prop="cycle" required>
          <el-input v-model="form.cycle" placeholder="例如: 每天8:00, 每周一9:00" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm">保存</el-button>
          <el-button @click="cancel">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { createReminder, updateReminder } from '@/api/reminder'
import type { Reminder } from '@/types'

const route = useRoute()
const router = useRouter()
const formRef = ref()

const form = ref<Omit<Reminder, 'reminder_id'>>({
  pid: Number(route.params.pid),
  reminder_type: '',
  cycle: '',
  next_reminder_date: '',
})

const formTitle = computed(() => {
  return route.params.id ? '编辑提醒' : '新增提醒'
})

const submitForm = async () => {
  try {
    if (route.params.id) {
      await updateReminder(Number(route.params.id), form.value.cycle)
    } else {
      await createReminder(form.value)
    }
    router.push({
      name: 'reminder-list',
      params: { pid: route.params.pid },
    })
  } catch (error) {
    console.error('保存提醒失败:', error)
  }
}

const cancel = () => {
  router.push({
    name: 'reminder-list',
    params: { pid: route.params.pid },
  })
}

onMounted(() => {
  if (route.params.id) {
    // TODO: 加载现有提醒数据
  }
})
</script>

<style scoped>
.reminder-form {
  padding: 20px;
}
.card-header {
  font-size: 18px;
  font-weight: bold;
}
</style>
