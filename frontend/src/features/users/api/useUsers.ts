import { useQuery } from '@tanstack/react-query'

import { listUsers } from '@/features/users/api/users.api'

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => listUsers(),
    staleTime: 60_000,
  })
}
