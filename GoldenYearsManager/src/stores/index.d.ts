
import 'pinia'

declare module 'pinia' {
  export interface PiniaCustomProperties {
    $auth: {
      hasRole(role: string): boolean
    }
  }
}

export interface LoginResponse {
  access_token: string
  token_type: string
}
