import { api } from '@/api/api'

export interface HealthBase {
  diseaseHistory?: string | null
  allergyHistory?: string | null
  bloodPressure?: string | null
  bloodGlucose?: number | string | null
  lastCheckupDate?: string | null
  medicalHistory?: string | null
}

export interface PersonDetail {
  pid: number
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
  checkOutDate?: string | null
  checkOutReason?: string | null
  photo: string
}

export interface PersonListItem {
  pid: number
  name: string
  gender: '男' | '女'
  age: number
  bedNumber: string
  category: '孤寡老人' | '残障人士' | '短期托管'
  checkInDate: string
  checkOutDate?: string | null
  photo: string
}

interface PersonListResponse {
  code: number
  total: number
  items: PersonListItem[]
  page: number
  page_size: number
}

export interface PersonDetailItem {
  personData: PersonDetail
  healthData: HealthBase
}

interface PersonDetailResponse {
  code: number
  data: PersonDetailItem
}

interface PersonCreateResponse {
  code: number
  message: string
  pid: number
}

interface BedNumber {
  pid: number
  bedNumber: string
}

interface BedNumberResponse {
  code: number
  total: number
  items: BedNumber[]
  page: number
  page_size: number
}

export interface PersonCreate {
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

export const personApi = {
  getList: (params: {
    name?: string | null
    category?: string | null
    status?: string
    page?: number
    page_size?: number
  }): Promise<PersonListResponse> => api.get('/persons', { params }).then(res => res.data),

  getDetail: (id: number): Promise<PersonDetailResponse> =>
    api.get(`/persons/person/${id}`).then(res => res.data),

  create: (data: {
    person_data: PersonCreate
    health_data: HealthBase
  }): Promise<PersonCreateResponse> => api.post('/persons', data),

  update: (id: number, data: {
    person_data: Partial<PersonCreate>
    health_data: HealthBase
  }): Promise<PersonCreateResponse> => api.put(`/persons/${id}`, data),

  delete: (id: number): Promise<void> => api.delete(`/persons/${id}`),

  getBedNumbers: (params: {
    page?: number
    page_size?: number
  }): Promise<BedNumberResponse> => api.get('/persons/get_bed_number', { params }).then(res => res.data)
}
