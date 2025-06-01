import { api } from '@/api/api'
import type { CareRecordForm } from '@/types'

interface Care {
  pid: number,
  caregiverId: number,
  careContent: string,
  careDate: string,
  evaluation: string,
  actualTime: string,
  careId: number
}

interface CareResponse {
  total: number
  items: Care[]
}

interface RequestParams {
  page?: number
  page_size?: number
}

// 创建护理记录
export const createCareRecord = (data: CareRecordForm & { plan_id?: number }) =>
  api.post('/care/', data)

// 获取护理记录
export const getCareRecord = (id: number) =>
  api.get(`/care/detail/${id}`).then(res => res.data) as Promise<Care>

// 获取患者护理记录
export const getPatientCareRecords = (params: RequestParams & { pid: number }) =>
  api.get(`/care/patient/${params.pid}`, { params }).then(res => res.data) as Promise<CareResponse>

// 获取护理员护理记录
export const getCaregiverRecords = (params: RequestParams & { caregiver_id: number }) =>
  api.get(`/care/caregiver/${params.caregiver_id}`, { params }).then(res => res.data) as Promise<CareResponse>

// 更新护理记录
export const updateCareRecord = (id: number, data: Partial<CareRecordForm>) =>
  api.put(`/care/${id}`, data)

// 删除护理记录
export const deleteCareRecord = (id: number) =>
  api.delete(`/care/${id}`)
