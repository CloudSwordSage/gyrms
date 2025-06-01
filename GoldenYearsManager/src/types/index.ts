export interface CarePlan {
  planId: number
  pid: number
  planName: string
  planContent: string
  frequency: string
  startDate: string
  endDate: string
  executorId: number | null
  status: '进行中' | '已结束' | '已放弃'
}

export interface CarePlanListParams {
  page?: number
  page_size?: number
  status?: string
  pid?: number
}

export interface CareRecord {
  care_id: number
  pid: number
  caregiver_id: number
  care_type?: string
  care_content: string
  care_date: string
  evaluation: string
  actual_time: string
  blood_pressure?: string
  blood_glucose?: string
  temperature?: string
}

export interface CareRecordHistory {
  modified_time: string
  modifier: string
  changes: string
}

export interface CareRecordForm {
  pid: number
  caregiver_id: number
  care_type?: string
  care_content: string
  care_date: string
  evaluation?: string
  blood_pressure?: string
  blood_glucose?: string
  temperature?: string
  plan_id?: number
}

export interface HealthRecord {
  health_id: number
  pid: number
  disease_history: string
  allergy_history: string
  blood_pressure: string
  blood_glucose: string
  last_checkup_date: string
  medical_history: string
}

export interface User {
  uid: number
  username: string
  realName: string
  role: '管理员' | '护理主任' | '护理工'
  phone: string
  isActivate: boolean
  createTime?: string
  lastLogin?: string
}

export interface CreateUser extends Omit<User, 'uid'> {
  password: string
}

export interface Reminder {
  reminder_id: number
  pid: number
  reminder_type: string
  cycle: string
  next_reminder_date: string
}
