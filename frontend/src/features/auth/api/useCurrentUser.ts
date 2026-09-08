import { useQuery } from '@tanstack/react-query'

import { fetchCurrentUser } from '@/features/auth/api/auth.api'
import { useAuthStore } from '@/features/auth/store/auth.store'

export function useCurrentUser() {
  const accessToken = useAuthStore((state) => state.accessToken)
  const setUser = useAuthStore((state) => state.setUser)

  return useQuery({
    queryKey: ['auth', 'me'],
    queryFn: async () => {
      const user = await fetchCurrentUser()
      setUser(user)
      return user
    },
    enabled: Boolean(accessToken),
    staleTime: 5 * 60_000,
  })
}
