<template>
  <div class="care-record-list">
    <el-card>
      <template #header>
        <div class="filter-header">
          <h3>患者护理记录</h3>
        </div>
      </template>

      <el-table :data="records" style="width: 100%">
        <el-table-column prop="careDate" label="日期" width="120" sortable />
        <el-table-column prop="careContent" label="护理内容" />
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button size="small" @click="viewDetail(row.careId)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="totalRecords"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getPatientCareRecords } from '@/api/care'

const props = defineProps<{
  pid: number
}>()

export interface CareRecord {
  careId: number
  pid: number
  caregiverId: number
  careType?: string
  careContent: string
  careDate: string
  evaluation: string
  actualTime: string
}

const records = ref<CareRecord[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const totalRecords = ref(0)

const TypeContent = (s: string) => {
  const [careType, careContent] = s.split(' <||> ')
  return {
    careType,
    careContent,
  }
}

const enrichCareData = async (plans: CareRecord[]) => {
  return Promise.all(
    plans.map(async (plan) => {
      try {
        const { careType, careContent } = TypeContent(plan.careContent)
        return {
          ...plan,
          careType: careType,
          careContent: careContent,
        }
      } catch (error) {
        console.error('获取人员详情失败:', error)
        return {
          ...plan,
          careType: '',
          careContent: plan.careContent,
        }
      }
    }),
  )
}
const fetchData = async () => {
  try {
    const res = await getPatientCareRecords({
      pid: props.pid,
      page: currentPage.value,
      page_size: pageSize.value,
    })
    records.value = await enrichCareData(res.items)
    totalRecords.value = res.total
  } catch (error) {
    console.error('获取护理记录失败:', error)
  }
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchData()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchData()
}

onMounted(fetchData)

const router = useRouter()

const viewDetail = (id: number) => {
  router.push(`/care-records/detail/${id}`)
}
</script>

<style scoped>
.care-record-list {
  padding: 20px;
}
.filter-header {
  display: flex;
  align-items: center;
}
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
