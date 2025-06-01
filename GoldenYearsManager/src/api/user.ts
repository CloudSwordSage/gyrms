import { api } from './api'
import type { User, CreateUser } from '@/types'

export const getUserList = (params: { skip?: number; limit?: number; role?: string, username?: string, name?: string }) =>
  api.get<User[]>('/user/', { params })

export const getUserDetail = (uid: number) =>
  api.get<User>(`/user/${uid}`)

export const createUser = (data: CreateUser) =>
  api.post<User>('/user/', data)

export const updateUser = (uid: number, data: Partial<User>) =>
  api.put<User>(`/user/${uid}`, data)

export const deleteUser = (uid: number) =>
  api.delete(`/user/${uid}`)
