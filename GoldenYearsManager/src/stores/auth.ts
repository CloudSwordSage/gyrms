import { defineStore } from 'pinia'
import { authApi } from '@/api/auth'
import type { User } from '@/types'

const TOKEN_KEY = 'gyrms_auth_token'
const PUBLIC_KEY_KEY = 'gyrms_public_key'
const USER_KEY = 'gyrms_user'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: (() => {
      const token = localStorage.getItem(TOKEN_KEY)
      return token && token !== 'undefined' ? token : null
    })(),
    publicKey: (() => {
      const key = localStorage.getItem(PUBLIC_KEY_KEY)
      return key && key !== 'undefined' ? key : null
    })(),
    user: (() => {
      try {
        const userData = localStorage.getItem(USER_KEY)
        return userData && userData !== 'undefined' ? JSON.parse(userData) as User : null
      } catch {
        return null
      }
    })()
  }),
  actions: {
    async getPublicKey() {
      try {
        const res = await authApi.getPublicKey()
        this.publicKey = res.data
        localStorage.setItem(PUBLIC_KEY_KEY, res.data)
        return res.data
      } catch (error) {
        console.error('获取公钥失败:', error)
        throw error
      }
    },
    async login(username: string, password: string) {
      try {
        if (!this.publicKey) {
          await this.getPublicKey()
        }
        const res = await authApi.login(username, password)
        this.token = res.accessToken
        localStorage.setItem(TOKEN_KEY, res.accessToken)

        // 获取当前用户信息
        const user = await authApi.getCurrentUser()
        this.user = user
        localStorage.setItem(USER_KEY, JSON.stringify(user))

        return true
      } catch (error) {
        console.error('登录失败:', error)
        return false
      }
    },
    async logout() {
      this.token = null
      this.publicKey = null
      this.user = null
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(PUBLIC_KEY_KEY)
      localStorage.removeItem(USER_KEY)
    },
    hasRole(role: string | string[]): boolean {
      if (!this.user || !this.user.role) {
        return false
      }

      if (Array.isArray(role)) {
        return role.some(r => this.user!.role === r)
      }
      return this.user.role === role
    }
  },
  getters: {
    isAuthenticated(): boolean {
      return !!this.token
    }
  }
})
