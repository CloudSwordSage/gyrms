declare module '*.vue' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<Record<string, never>, Record<string, never>, unknown>
  export default component
}

declare module '@/stores/auth' {
  import { StoreDefinition } from 'pinia'
  export const useAuthStore: StoreDefinition<
    'auth',
    {
      token: string | null
      publicKey: string | null
      user: {
        uid: number
        username: string
        real_name: string
        role: string
        phone: string
        is_activate: boolean
      } | null
    },
    {
      isAuthenticated: boolean
    },
    {
      getPublicKey(): Promise<string>
      login(username: string, password: string): Promise<boolean>
      logout(): Promise<void>
      hasRole(role: string): boolean
    }
  >
}
