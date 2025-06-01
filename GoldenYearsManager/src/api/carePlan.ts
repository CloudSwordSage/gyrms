import { api } from '@/api/api'
import type { CarePlan, CarePlanListParams } from '@/types'

interface CarePlanResponse {
  total: number
  items: CarePlan[]
}

export const carePlanApi = {
  createCarePlan: (data: Omit<CarePlan, 'planId'>): Promise<CarePlan> =>
    api.post('/care_plan/', data).then(res => res.data),

  getAvailablePlans: ( params?: CarePlanListParams ): Promise<CarePlanResponse> =>
    api.get('/care_plan/available', { params }).then(res => res.data),

  acceptPlan: (planId: number): Promise<CarePlan> =>
    api.post(`/care_plan/${planId}/accept`).then(res => res.data),

  abandonPlan: (planId: number): Promise<CarePlan> =>
    api.post(`/care_plan/${planId}/abandon`).then(res => res.data),

  transferPlan: (
    planId: number,
    newExecutorId: number
  ): Promise<CarePlan> =>
    api.post(`/care_plan/${planId}/transfer`, { newExecutorId: newExecutorId }).then(res => res.data),

  assignPlan: (
    planId: number,
    executorId: number,
    assignType: string
  ): Promise<CarePlan> =>
    api.post(`/care_plan/${planId}/assign`, { executorId: executorId, assignType: assignType }).then(res => res.data),

  getMyPlans: (params?: CarePlanListParams): Promise<CarePlanResponse> =>
    api.get('/care_plan/my', { params }).then(res => res.data),

  getAllPlans: (params?: CarePlanListParams): Promise<CarePlanResponse> =>
    api.get('/care_plan/all', { params }).then(res => res.data),

  completePlan: (planId: number): Promise<CarePlan> =>
    api.post(`/care_plan/${planId}/complete`).then(res => res.data),

  getPlan: (planId: number): Promise<CarePlan> =>
    api.get(`/care_plan/detail/${planId}`).then(res => res.data)
};
