import { api } from './api'
import type { Reminder } from '@/types'

interface ReminderListResponse {
  total: number
  items: Reminder[]
  page: number
  page_size: number
}

export const getReminderList = (pid: number, params?: {
  page?: number
  page_size?: number
}) => api.get<ReminderListResponse>(`/reminder/${pid}`, { params })

export const createReminder = (data: Omit<Reminder, 'reminder_id'>) =>
  api.post<Reminder>('/reminder/', data)

export const updateReminder = (id: number, cycle: string) =>
  api.put<Reminder>(`/reminder/${id}`, { cycle })

export const deleteReminder = (id: number) =>
  api.delete(`/reminder/${id}`)
