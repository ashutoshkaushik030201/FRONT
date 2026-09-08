import { create } from 'zustand'
import { persist } from 'zustand/middleware'

import type { User } from '@/domain/types/user'

interface AuthState {
  accessToken: string | null
  refreshToken: string | null
  user: User | null
  setSession: (tokens: { accessToken: string; refreshToken: string }) => void
  setUser: (user: User | null) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      accessToken: null,
      refreshToken: null,
      user: null,
      setSession: ({ accessToken, refreshToken }) => set({ accessToken, refreshToken }),
      setUser: (user) => set({ user }),
      logout: () => set({ accessToken: null, refreshToken: null, user: null }),
    }),
    {
      name: 'nexus-auth',
      partialize: (state) => ({
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        user: state.user,
      }),
    },
  ),
)

/** Non-hook accessor for use outside React components (e.g. the API client interceptors). */
export const authStore = {
  getState: useAuthStore.getState,
  subscribe: useAuthStore.subscribe,
}
