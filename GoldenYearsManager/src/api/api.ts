/*
* @Time    : 2025/4/28 12:16:48
* @Author  : 墨烟行(GitHub UserName: CloudSwordSage)
* @File    : api.ts
* @Desc    : API配置，包含请求/响应拦截器和数据格式转换
*/

import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

type RecursiveObject<T> = T extends (infer U)[]
  ? RecursiveObject<U>[]
  : T extends object
  ? { [K in keyof T]: RecursiveObject<T[K]> }
  : T

// 驼峰转蛇形
function camelToSnake<T>(obj: T): RecursiveObject<T> {
  if (obj === null || typeof obj !== 'object') return obj as RecursiveObject<T>

  if (Array.isArray(obj)) {
    return obj.map(item => camelToSnake(item)) as RecursiveObject<T>
  }

  return Object.keys(obj as object).reduce((acc, key) => {
    const snakeKey = key.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`)
    acc[snakeKey] = camelToSnake((obj as Record<string, unknown>)[key])
    return acc
  }, {} as Record<string, unknown>) as RecursiveObject<T>
}

// 蛇形转驼峰
function snakeToCamel<T>(obj: T): RecursiveObject<T> {
  if (obj === null || typeof obj !== 'object') return obj as RecursiveObject<T>

  if (Array.isArray(obj)) {
    return obj.map(item => snakeToCamel(item)) as RecursiveObject<T>
  }

  return Object.keys(obj as object).reduce((acc, key) => {
    const camelKey = key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase())
    acc[camelKey] = snakeToCamel((obj as Record<string, unknown>)[key])
    return acc
  }, {} as Record<string, unknown>) as RecursiveObject<T>
}

export const api = axios.create({
  baseURL: "http://api.cloudswordsage.top:8000/api",
  timeout: 10000
})

// 请求拦截器
api.interceptors.request.use(config => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }

  // 转换请求数据为蛇形格式
  if (config.data) {
    config.data = camelToSnake(config.data)
  }

  // 转换GET参数为蛇形格式
  if (config.params) {
    config.params = camelToSnake(config.params)
  }

  return config
})

// 响应拦截器
api.interceptors.response.use(
  response => {
    // 转换响应数据为驼峰格式
    if (response.data) {
      response.data = snakeToCamel(response.data)
    }
    // console.log('响应拦截器 - 响应数据:', response.data)
    return response
  },
  error => {
    console.error('响应拦截器 - 错误:', error)
    if (error.response?.status === 401) {
      // Token过期处理
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
