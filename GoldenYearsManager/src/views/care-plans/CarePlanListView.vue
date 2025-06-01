<template>
  <div class="care-plan-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>护理计划大厅</h2>
          <el-button type="primary" @click="handleMy" v-if="authStore.hasRole('护理工')">
            我的护理计划
          </el-button>
          <el-button
            type="primary"
            @click="handleCreate"
            v-if="authStore.hasRole('管理员') || authStore.hasRole('护理主任')"
          >
            新建护理计划
          </el-button>
        </div>
      </template>

      <el-table :data="planList" border style="width: 100%" v-loading="loading">
        <el-table-column prop="planId" label="ID" width="80" />
        <el-table-column prop="planName" label="计划名称" />
        <el-table-column prop="Name" label="护理对象" width="120" />
        <el-table-column prop="bedNumber" label="床号" width="100" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="startDate" label="开始日期" width="120" />
        <el-table-column prop="endDate" label="结束日期" width="120" />
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button size="small" @click="handleDetail(row.planId)">详情</el-button>
            <el-button
              size="small"
              type="primary"
              v-if="
                row.status === '进行中' &&
                (authStore.hasRole('管理员') || authStore.hasRole('护理主任'))
              "
              @click="handleComplete(row.planId)"
            >
              完成
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="fetchPlans"
        @size-change="fetchPlans"
      />
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { carePlanApi } from '@/api/carePlan'
import { personApi } from '@/api/person'
import { ElMessage } from 'element-plus'
import type { CarePlan } from '@/types'

const authStore = useAuthStore()
const router = useRouter()

const planList = ref<CarePlan[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const loading = ref(false)

const statusTagType = (status: '进行中' | '已结束' | '已放弃') => {
  const map = {
    进行中: 'primary',
    已结束: 'success',
    已放弃: 'danger',
  }
  return map[status]
}

const enrichPlanData = async (plans: CarePlan[]) => {
  return Promise.all(
    plans.map(async (plan) => {
      try {
        const user = await personApi.getDetail(plan.pid)
        return {
          ...plan,
          Name: user.data.personData.name,
          bedNumber: user.data.personData.bedNumber,
        }
      } catch (error) {
        console.error('获取人员详情失败:', error)
        return {
          ...plan,
          Name: '未知',
          bedNumber: '--',
        }
      }
    }),
  )
}

const PlansItems =
  authStore.hasRole('管理员') || authStore.hasRole('护理主任')
    ? carePlanApi.getAllPlans
    : carePlanApi.getAvailablePlans

const fetchPlans = async () => {
  try {
    loading.value = true
    const response = await PlansItems({
      page: currentPage.value,
      page_size: pageSize.value,
    })

    const enrichedPlans = await enrichPlanData(response.items)
    planList.value = enrichedPlans
    total.value = response.total
  } catch (error) {
    console.error('获取护理计划失败:', error)
    ElMessage.error('获取护理计划列表失败')
  } finally {
    loading.value = false
  }
}

const handleCreate = () => {
  router.push({ name: 'care-plan-create' })
}

const handleMy = () => {
  router.push({ name: 'my-care-plan-list' })
}

const handleDetail = (id: number) => {
  router.push({ name: 'care-plan-detail', params: { id } })
}

const handleComplete = async (id: number) => {
  try {
    await carePlanApi.completePlan(id)
    ElMessage.success('护理计划已完成')
    await fetchPlans()
  } catch (error) {
    console.error('完成护理计划失败:', error)
    ElMessage.error('完成护理计划失败')
  }
}

onMounted(() => {
  fetchPlans()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
