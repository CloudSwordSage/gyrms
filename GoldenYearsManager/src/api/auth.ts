import { api } from '@/api/api'
import { encrypt } from '@/utils/encrypt'
import type { User } from '@/types'

interface PublicKeyResponse {
  code: number
  data: string
  message: string
}

interface LoginResponse {
  accessToken: string
  tokenType: string
}

export const authApi = {
  getPublicKey: (): Promise<PublicKeyResponse> =>
    api.get('/auth/public_key').then(res => res.data).catch(error => {
    console.error('获取公钥失败:', error)
    throw new Error('无法获取公钥，请检查API服务')
  }),
  login: async (username: string, password: string): Promise<LoginResponse> => {
    const {data: publicKey} = await authApi.getPublicKey()
    const encrypted = encrypt(password, publicKey)
    const response = await api.post('/auth/login', {
      username: username,
      password: encrypted
    })
    return response.data
  },
  getCurrentUser: (): Promise<User> =>
    api.get('/auth/me').then(res => res.data),
  verifyToken: (data: {token: string}) =>
    api.post('/auth/verify_token', data).then(res => res.data)
}
