import { apiClient } from '@/shared/lib/api-client'
import type { User } from '@/domain/types/user'

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export async function loginRequest(email: string, password: string): Promise<TokenResponse> {
  const body = new URLSearchParams()
  body.set('username', email)
  body.set('password', password)

  const { data } = await apiClient.post<TokenResponse>('/auth/login', body, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return data
}

export async function fetchCurrentUser(): Promise<User> {
  const { data } = await apiClient.get<User>('/auth/me')
  return data
}
