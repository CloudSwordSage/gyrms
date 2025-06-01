<template>
  <div class="reminder-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>提醒列表</span>
          <el-button type="primary" @click="createReminder">新增提醒</el-button>
        </div>
      </template>

      <el-table :data="reminders" v-loading="loading">
        <el-table-column prop="reminder_type" label="提醒类型" />
        <el-table-column prop="cycle" label="周期" />
        <el-table-column prop="next_reminder_date" label="下次提醒日期" />
        <el-table-column label="操作" width="180">
          <template #default="scope">
            <el-button size="small" @click="editReminder(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteReminder(scope.row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        @current-change="fetchData"
        layout="total, prev, pager, next"
      />
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getReminderList, deleteReminder as deleteReminderApi } from '@/api/reminder'
import type { Reminder } from '@/types'

const route = useRoute()
const router = useRouter()

const reminders = ref<Reminder[]>([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

const fetchData = async () => {
  loading.value = true
  try {
    const res = await getReminderList(Number(route.params.pid), {
      page: page.value,
      page_size: pageSize.value,
    })
    reminders.value = res.data.items
    total.value = res.data.total
  } catch (error) {
    console.error('获取提醒列表失败:', error)
  } finally {
    loading.value = false
  }
}

const createReminder = () => {
  router.push({
    name: 'reminder-create',
    params: { pid: route.params.pid },
  })
}

const editReminder = (reminder: Reminder) => {
  router.push({
    name: 'reminder-edit',
    params: { id: reminder.reminder_id },
  })
}

const deleteReminder = async (reminder: Reminder) => {
  try {
    await deleteReminderApi(reminder.reminder_id)
    await fetchData()
  } catch (error) {
    console.error('删除提醒失败:', error)
  }
}

onMounted(fetchData)
</script>

<style scoped>
.reminder-list {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
