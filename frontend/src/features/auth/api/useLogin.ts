import { useMutation } from '@tanstack/react-query'

import { fetchCurrentUser, loginRequest } from '@/features/auth/api/auth.api'
import { useAuthStore } from '@/features/auth/store/auth.store'

export function useLogin() {
  const setSession = useAuthStore((state) => state.setSession)
  const setUser = useAuthStore((state) => state.setUser)

  return useMutation({
    mutationFn: async ({ email, password }: { email: string; password: string }) => {
      const tokens = await loginRequest(email, password)
      setSession({ accessToken: tokens.access_token, refreshToken: tokens.refresh_token })
      const user = await fetchCurrentUser()
      setUser(user)
      return user
    },
  })
}
