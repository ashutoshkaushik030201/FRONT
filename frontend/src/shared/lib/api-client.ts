import axios, { AxiosError, type InternalAxiosRequestConfig } from 'axios'

import { authStore } from '@/features/auth/store/auth.store'
import { env } from '@/shared/lib/env'

export const apiClient = axios.create({
  baseURL: env.apiBaseUrl,
})

apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const { accessToken } = authStore.getState()
  if (accessToken) {
    config.headers.set('Authorization', `Bearer ${accessToken}`)
  }
  return config
})

/** Set by the app shell so the interceptor can navigate without a hard page reload. */
let unauthorizedHandler: (() => void) | null = null

export function setUnauthorizedHandler(handler: () => void) {
  unauthorizedHandler = handler
}

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      authStore.getState().logout()
      if (unauthorizedHandler) {
        unauthorizedHandler()
      } else {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  },
)

export interface ApiErrorBody {
  error?: { code: string; message: string; details?: Record<string, unknown> }
  detail?: string
}

export function extractErrorMessage(error: unknown, fallback = 'Something went wrong'): string {
  if (axios.isAxiosError(error)) {
    const body = error.response?.data as ApiErrorBody | undefined
    return body?.error?.message ?? body?.detail ?? fallback
  }
  return fallback
}
