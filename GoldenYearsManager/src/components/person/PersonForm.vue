<template>
  <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-select v-model="form.gender">
            <el-option label="男" value="男" />
            <el-option label="女" value="女" />
          </el-select>
        </el-form-item>
        <el-form-item label="年龄" prop="age">
          <el-input-number v-model="form.age" :min="0" />
        </el-form-item>
        <el-form-item label="身份证号" prop="idCard">
          <el-input v-model="form.idCard" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="紧急联系人" prop="emergencyContact">
          <el-input v-model="form.emergencyContact" />
        </el-form-item>
        <el-form-item label="紧急联系电话" prop="emergencyPhone">
          <el-input v-model="form.emergencyPhone" />
        </el-form-item>
      </el-col>

      <el-col :span="12">
        <el-form-item label="照片">
          <el-upload
            action="#"
            :auto-upload="false"
            :on-change="handleImageChange"
            :show-file-list="false"
          >
            <img v-if="form.photo" :src="form.photo" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="床位号" prop="bedNumber">
          <el-input v-model="form.bedNumber" />
        </el-form-item>
        <el-form-item label="人员类型" prop="category">
          <el-select v-model="form.category">
            <el-option label="孤寡老人" value="孤寡老人" />
            <el-option label="残障人士" value="残障人士" />
            <el-option label="短期托管" value="短期托管" />
          </el-select>
        </el-form-item>
        <el-form-item label="入院日期" prop="checkInDate">
          <el-date-picker
            v-model="form.checkInDate"
            type="date"
            placeholder="选择日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
      </el-col>
    </el-row>

    <el-divider>健康信息</el-divider>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="病史" prop="diseaseHistory">
          <el-input v-model="form.diseaseHistory" type="textarea" />
        </el-form-item>
        <el-form-item label="过敏史" prop="allergyHistory">
          <el-input v-model="form.allergyHistory" type="textarea" />
        </el-form-item>
        <el-form-item label="治疗史" prop="medicalHistory">
          <el-input v-model="form.medicalHistory" type="textarea" />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="血压" prop="bloodPressure">
          <el-input v-model="form.bloodPressure" placeholder="例如: 120/80" />
        </el-form-item>
        <el-form-item label="血糖(mmol/L)" prop="bloodGlucose">
          <el-input-number v-model="form.bloodGlucose" :min="0" :step="0.1" />
        </el-form-item>
        <el-form-item label="上次体检时间" prop="lastCheckupDate">
          <el-date-picker
            v-model="form.lastCheckupDate"
            type="date"
            placeholder="选择日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
      </el-col>
    </el-row>

    <el-form-item>
      <el-button type="primary" @click="submitForm">提交</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'
import type { FormInstance, UploadFile } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

import type { PersonCreate, HealthBase } from '@/api/person'

export interface PersonForm {
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
  diseaseHistory?: string | null
  allergyHistory?: string | null
  bloodPressure?: string | null
  bloodGlucose?: number | string | null
  lastCheckupDate?: string | null
  medicalHistory?: string | null
}

const props = defineProps<{
  initialData?: Partial<PersonForm>
}>()

console.log('props.initialData: ', props.initialData)

const emit = defineEmits(['submit'])

const formRef = ref<FormInstance>()
const form = ref<PersonForm>({
  ...{
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
    diseaseHistory: null,
    allergyHistory: null,
    bloodPressure: null,
    bloodGlucose: null,
    lastCheckupDate: null,
    medicalHistory: null,
  },
  ...props.initialData,
})

// 监听 initialData 变化
watch(
  () => props.initialData,
  (newData) => {
    if (newData) {
      form.value = {
        ...form.value,
        ...newData,
      }
    }
  },
  { deep: true },
)

const toApiData = (formData: PersonForm) => ({
  person_data: {
    name: formData.name,
    gender: formData.gender,
    age: formData.age,
    idCard: formData.idCard,
    phone: formData.phone,
    emergencyContact: formData.emergencyContact,
    emergencyPhone: formData.emergencyPhone,
    bedNumber: formData.bedNumber,
    category: formData.category,
    checkInDate: formData.checkInDate,
    photo: formData.photo,
  } as PersonCreate,
  health_data: {
    diseaseHistory: formData.diseaseHistory,
    allergyHistory: formData.allergyHistory,
    bloodPressure: formData.bloodPressure,
    bloodGlucose: formData.bloodGlucose,
    lastCheckupDate: formData.lastCheckupDate,
    medicalHistory: formData.medicalHistory,
  } as HealthBase,
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  age: [{ required: true, message: '请输入年龄', trigger: 'blur' }],
  idCard: [
    { required: true, message: '请输入身份证号', trigger: 'blur' },
    { pattern: /^\d{17}[\dXx]$/, message: '请输入有效的身份证号', trigger: 'blur' },
  ],
  phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号', trigger: 'blur' },
  ],
  emergencyContact: [{ required: true, message: '请输入紧急联系人', trigger: 'blur' }],
  emergencyPhone: [
    { required: true, message: '请输入紧急联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号', trigger: 'blur' },
  ],
  bedNumber: [{ required: true, message: '请输入床位号', trigger: 'blur' }],
  category: [{ required: true, message: '请选择人员类型', trigger: 'change' }],
  checkInDate: [{ required: true, message: '请选择入院日期', trigger: 'change' }],
  bloodPressure: [{ pattern: /^\d{1,3}\/\d{1,3}$/, message: '格式应为120/80', trigger: 'blur' }],
  bloodGlucose: [
    { type: 'number', min: 0, max: 30, message: '血糖值应在0-30之间', trigger: 'blur' },
  ],
  lastCheckupDate: [{ message: '请选择上次体检时间', trigger: 'change' }],
  medicalHistory: [{ message: '请输入治疗史', trigger: 'blur' }],
}

const handleImageChange = (file: UploadFile) => {
  if (file.raw) {
    if (file.raw.size > 2 * 1024 * 1024) {
      ElMessage.error('图片大小不能超过2MB')
      return
    }
    if (!['image/jpeg', 'image/png'].includes(file.raw.type)) {
      ElMessage.error('只支持JPG/PNG格式图片')
      return
    }

    const reader = new FileReader()
    reader.onload = (e) => {
      if (e.target?.result) {
        form.value.photo = e.target.result as string
      }
    }
    reader.readAsDataURL(file.raw)
  }
}

const submitForm = async () => {
  try {
    await formRef.value?.validate()
    emit('submit', toApiData(form.value))
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}
</script>

<style scoped>
.avatar {
  width: 120px;
  height: 120px;
  display: block;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 120px;
  height: 120px;
  line-height: 120px;
  text-align: center;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
}
</style>
