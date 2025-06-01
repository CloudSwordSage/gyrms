<template>
  <div>
    <el-page-header @back="goBack" content="人员详情" />
    <el-divider />

    <el-form :model="person" label-width="120px">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="姓名">
            <el-input v-model="person.personData.name" readonly />
          </el-form-item>
          <el-form-item label="性别">
            <el-input v-model="person.personData.gender" readonly />
          </el-form-item>
          <el-form-item label="年龄">
            <el-input v-model="person.personData.age" readonly />
          </el-form-item>
          <el-form-item label="联系电话">
            <el-input v-model="person.personData.phone" readonly />
          </el-form-item>
          <el-form-item label="紧急联系人">
            <el-input v-model="person.personData.emergencyContact" readonly />
          </el-form-item>
          <el-form-item label="紧急联系电话">
            <el-input v-model="person.personData.emergencyPhone" readonly />
          </el-form-item>
        </el-col>

        <el-col :span="12">
          <el-form-item label="照片">
            <img v-if="person.personData.photo" :src="person.personData.photo" class="avatar" />
            <div v-else class="avatar-placeholder">无照片</div>
          </el-form-item>
          <el-form-item label="床位号">
            <el-input v-model="person.personData.bedNumber" readonly />
          </el-form-item>
          <el-form-item label="人员类型">
            <el-input v-model="person.personData.category" readonly />
          </el-form-item>
          <el-form-item label="入院日期">
            <el-input v-model="person.personData.checkInDate" readonly />
          </el-form-item>
        </el-col>
      </el-row>

      <el-divider>健康信息</el-divider>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="病史">
            <el-input v-model="person.healthData.diseaseHistory" type="textarea" readonly />
          </el-form-item>
          <el-form-item label="过敏史">
            <el-input v-model="person.healthData.allergyHistory" type="textarea" readonly />
          </el-form-item>
          <el-form-item label="治疗史">
            <el-input v-model="person.healthData.medicalHistory" type="textarea" readonly />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="血压">
            <el-input v-model="person.healthData.bloodPressure" readonly />
          </el-form-item>
          <el-form-item label="血糖(mmol/L)">
            <el-input v-model="person.healthData.bloodGlucose" readonly />
          </el-form-item>
          <el-form-item label="上次体检时间">
            <el-input v-model="person.healthData.lastCheckupDate" readonly />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { personApi, type PersonDetailItem } from '@/api/person'

const route = useRoute()
const router = useRouter()

const person = ref<PersonDetailItem>({
  personData: {
    pid: 0,
    name: '',
    gender: '男',
    age: 60,
    idCard: '',
    phone: '',
    emergencyContact: '',
    emergencyPhone: '',
    bedNumber: '',
    category: '孤寡老人',
    checkInDate: '',
    photo: '',
  },
  healthData: {
    diseaseHistory: '',
    allergyHistory: '',
    bloodPressure: '',
    bloodGlucose: 0,
    lastCheckupDate: '',
    medicalHistory: '',
  },
})

const goBack = () => {
  router.go(-1)
}

onMounted(async () => {
  const id = route.params.id as string
  if (id) {
    const data = await personApi.getDetail(Number(id))
    person.value = data.data
    console.log(person.value)
  }
})
</script>

<style scoped>
.avatar {
  width: 120px;
  height: 120px;
  display: block;
}
.avatar-placeholder {
  width: 120px;
  height: 120px;
  line-height: 120px;
  text-align: center;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  color: #8c939d;
}
</style>
