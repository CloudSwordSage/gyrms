<template>
  <div class="care-plan-detail">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>护理计划详情</h2>
          <div class="actions" v-if="planData.status === '进行中'">
            <el-button type="primary" @click="handleAccept" v-if="!planData.executorId">
              接取
            </el-button>
            <el-button
              type="warning"
              @click="handleTransfer"
              v-if="planData.executorId === authStore.user?.uid"
            >
              转交
            </el-button>
            <el-button
              type="danger"
              @click="handleAbandon"
              v-if="planData.executorId === authStore.user?.uid"
            >
              放弃
            </el-button>
            <el-button
              type="success"
              @click="handleAddCareRecord"
              v-if="planData.executorId === authStore.user?.uid"
            >
              添加护理记录
            </el-button>
          </div>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="计划ID">{{ planData.planId }}</el-descriptions-item>
        <el-descriptions-item label="计划名称">{{ planData.planName }}</el-descriptions-item>
        <el-descriptions-item label="护理对象">{{ planData.name }}</el-descriptions-item>
        <el-descriptions-item label="床位号">{{ planData.bedNumber }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="statusTagType(planData.status as PlanStatus)">
            {{ planData.status }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="执行人">{{
          planData.executorName || '未分配'
        }}</el-descriptions-item>
        <el-descriptions-item label="开始日期">{{ planData.startDate }}</el-descriptions-item>
        <el-descriptions-item label="结束日期">{{ planData.endDate }}</el-descriptions-item>
        <el-descriptions-item label="执行频率">{{ planData.frequency }}</el-descriptions-item>
        <el-descriptions-item label="计划内容" :span="2">
          <div class="plan-content">{{ planData.planContent }}</div>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { carePlanApi } from '@/api/carePlan'
import { getUserDetail } from '@/api/user'
import { personApi } from '@/api/person'
import { ElMessageBox, ElMessage } from 'element-plus'
import type { CarePlan } from '@/types/index'

type PlanStatus = CarePlan['status']

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()
const id = Number(route.params.id)

const planData = ref<
  CarePlan & {
    executorName: string
    name: string
    bedNumber: string
  }
>({
  planId: 0,
  pid: 0,
  planName: '',
  planContent: '',
  frequency: '',
  startDate: '',
  endDate: '',
  status: '进行中',
  executorId: null,
  executorName: '',
  name: '',
  bedNumber: '',
})

const getCurrentExecutorName = async (executorId: number | null) => {
  if (!executorId) {
    return '未分配'
  }

  const executor = await getUserDetail(executorId)
  return executor.data.realName
}

const enrichPlanData = async (plan: CarePlan) => {
  try {
    const user = await personApi.getDetail(plan.pid)
    return {
      ...plan,
      name: user.data.personData.name,
      bedNumber: user.data.personData.bedNumber,
    }
  } catch (error) {
    console.error('获取人员详情失败:', error)
    return {
      ...plan,
      name: '未知',
      bedNumber: '--',
    }
  }
}

const fetchPlanDetail = async () => {
  try {
    const response = await carePlanApi.getPlan(id)
    if (!response) {
      throw new Error('未找到该护理计划')
    }
    const plan = await enrichPlanData(response)

    const {
      planId,
      pid,
      planName,
      planContent,
      frequency,
      startDate,
      endDate,
      status,
      executorId,
      name,
      bedNumber,
    } = plan
    const currentExecutorName = await getCurrentExecutorName(executorId)
    planData.value = {
      planId,
      pid,
      planName,
      planContent,
      frequency,
      startDate,
      endDate,
      status,
      executorId,
      executorName: currentExecutorName,
      name,
      bedNumber,
    }
  } catch (error) {
    console.error('获取护理计划详情失败:', error)
    ElMessage.error('获取护理计划详情失败')
  }
}

const statusTagType = (status: PlanStatus) => {
  const map = {
    进行中: 'primary',
    已结束: 'success',
    已放弃: 'danger',
  }
  return map[status] || ''
}

const handleAccept = async () => {
  try {
    await carePlanApi.acceptPlan(id)
    await fetchPlanDetail()
  } catch (error) {
    console.error('接取护理计划失败:', error)
  }
}

const handleTransfer = async () => {
  try {
    const { value: toUserId } = await ElMessageBox.prompt('请输入要转交的用户ID', '转交护理计划', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputPattern: /^\d+$/,
      inputErrorMessage: '请输入有效的用户ID',
    })

    await carePlanApi.transferPlan(id, Number(toUserId))
    ElMessage.success('护理计划已成功转交')
    await fetchPlanDetail()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('转交护理计划失败:', error)
      ElMessage.error('转交护理计划失败')
    }
  }
}

const handleAbandon = async () => {
  try {
    await carePlanApi.abandonPlan(id)
    await fetchPlanDetail()
  } catch (error) {
    console.error('放弃护理计划失败:', error)
  }
}

const handleAddCareRecord = () => {
  if (!planData.value.pid) {
    ElMessage.error('无法获取护理对象ID')
    return
  }
  router.push({
    name: 'care-record-create',
    params: { pid: planData.value.pid.toString() },
    query: { planId: planData.value.planId.toString() },
  })
}

onMounted(() => {
  fetchPlanDetail()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.plan-content {
  white-space: pre-wrap;
  line-height: 1.6;
}
</style>
