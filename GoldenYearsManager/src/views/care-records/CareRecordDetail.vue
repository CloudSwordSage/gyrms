<template>
  <div class="care-record-detail">
    <el-card>
      <template #header>
        <div class="card-header">
          <el-button @click="goBack">返回</el-button>
        </div>
      </template>

      <el-descriptions :column="1" border>
        <el-descriptions-item label="姓名">
          {{ record.name }}
        </el-descriptions-item>
        <el-descriptions-item label="床号">
          {{ record.bed_number }}
        </el-descriptions-item>
        <el-descriptions-item label="护理类型">
          {{ getCareTypeName(record.care_type) }}
        </el-descriptions-item>
        <el-descriptions-item label="护理日期">
          {{ record.care_date }}
        </el-descriptions-item>
        <el-descriptions-item label="护理内容">
          <pre>{{ record.care_content }}</pre>
        </el-descriptions-item>
        <el-descriptions-item label="评估">
          <pre>{{ record.evaluation || '无' }}</pre>
        </el-descriptions-item>
        <el-descriptions-item label="记录时间">
          {{ record.actual_time }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCareRecord } from '@/api/care'
import type { CareRecord } from '@/types'
import { personApi } from '@/api/person'

const route = useRoute()
const router = useRouter()

const record = ref<
  CareRecord & {
    name: string
    bed_number: string
  }
>({
  care_id: 0,
  pid: 0,
  caregiver_id: 0,
  care_type: '',
  care_content: '',
  care_date: '',
  evaluation: '',
  actual_time: '',
  name: '',
  bed_number: '',
})

const loading = ref(false)

const getCareTypeName = (type?: string) => {
  switch (type) {
    case 'daily':
      return '日常护理'
    case 'medical':
      return '医疗护理'
    case 'recovery':
      return '康复护理'
    default:
      return '未分类'
  }
}

const TypeContent = (s: string) => {
  const [careType, careContent] = s.split(' <||> ')
  return {
    careType,
    careContent,
  }
}

const fetchData = async () => {
  loading.value = true
  try {
    const id = Number(route.params.id)
    const res = await getCareRecord(id)
    const user = await personApi.getDetail(res.pid)
    const { careType, careContent } = TypeContent(res.careContent)
    if (res) {
      record.value.care_id = res.careId
      record.value.pid = res.pid
      record.value.caregiver_id = res.caregiverId
      record.value.care_type = careType
      record.value.care_content = careContent
      record.value.care_date = res.careDate
      record.value.evaluation = res.evaluation
      record.value.actual_time = res.actualTime
      record.value.name = user.data.personData.name
      record.value.bed_number = user.data.personData.bedNumber
    }
  } catch (error) {
    console.error('获取护理记录失败:', error)
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.go(-1)
}

onMounted(fetchData)
</script>

<style scoped>
.care-record-detail {
  padding: 20px;
}
pre {
  white-space: pre-wrap;
  margin: 0;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
