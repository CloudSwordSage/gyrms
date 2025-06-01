<template>
  <div class="person-edit">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>编辑人员</span>
        </div>
      </template>

      <PersonFormComponent
        v-if="Object.keys(formData).length > 0"
        :initial-data="formData"
        @submit="handleSubmit"
      />
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { useRoute, useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import PersonFormComponent from '@/components/person/PersonForm.vue'
import type { PersonForm } from '@/components/person/PersonForm.vue'
import { personApi } from '@/api/person'
import type { PersonDetailItem } from '@/api/person'

const route = useRoute()
const router = useRouter()
const id = Number(route.params.id)

const formData = ref<Partial<PersonForm>>({})

interface PersonData {
  name: string
  gender: '男' | '女'
  age: number
  idCard: string
  phone: string
  emergencyContact: string
  emergencyPhone: string
  bedNumber: string
  category: '孤寡老人' | '残障人士' | '短期托管'
  checkInDate: string
  photo: string
}

interface HealthData {
  diseaseHistory?: string
  allergyHistory?: string
  bloodPressure?: string
  bloodGlucose?: number
  lastCheckupDate?: string
  medicalHistory?: string
}

interface PersonPutData {
  person_data: PersonData
  health_data: HealthData
}

const toFormData = (detail: PersonDetailItem): Partial<PersonForm> => ({
  ...detail.personData,
  ...detail.healthData,
})

onMounted(async () => {
  try {
    const { data } = await personApi.getDetail(id)
    console.log('获取人员详情成功:', data)
    console.log('编码: ', toFormData(data))
    formData.value = toFormData(data)
    console.log('formData:', formData.value)
  } catch (error) {
    console.error('获取人员详情失败:', error)
  }
})

const handleSubmit = async (form: PersonPutData) => {
  try {
    console.log('提交人员信息:', form)
    await personApi.update(id, form)
    router.push('/person')
  } catch (error) {
    console.error('更新人员失败:', error)
  }
}
</script>

<style scoped>
.person-edit {
  padding: 20px;
}
</style>
