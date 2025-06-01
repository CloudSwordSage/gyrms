<template>
  <div class="person-create">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>新增人员</span>
        </div>
      </template>

      <PersonFormComponent @submit="handleSubmit" />
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router'
import PersonFormComponent from '@/components/person/PersonForm.vue'
import { personApi } from '@/api/person'

const router = useRouter()

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

interface PersonCreateData {
  person_data: PersonData
  health_data: HealthData
}

const handleSubmit = async (formData: PersonCreateData) => {
  try {
    console.log('提交数据:', formData)
    await personApi.create({
      person_data: {
        name: formData.person_data.name,
        gender: formData.person_data.gender,
        age: formData.person_data.age,
        idCard: formData.person_data.idCard,
        phone: formData.person_data.phone,
        emergencyContact: formData.person_data.emergencyContact,
        emergencyPhone: formData.person_data.emergencyPhone,
        bedNumber: formData.person_data.bedNumber,
        category: formData.person_data.category,
        checkInDate: formData.person_data.checkInDate,
        photo: formData.person_data.photo,
      },
      health_data: {
        diseaseHistory: formData.health_data.diseaseHistory,
        allergyHistory: formData.health_data.allergyHistory,
        bloodPressure: formData.health_data.bloodPressure,
        bloodGlucose: formData.health_data.bloodGlucose,
        lastCheckupDate: formData.health_data.lastCheckupDate,
        medicalHistory: formData.health_data.medicalHistory,
      },
    })
    router.push('/person')
  } catch (error) {
    console.error('创建人员失败:', error)
  }
}
</script>

<style scoped>
.person-create {
  padding: 20px;
}
</style>
