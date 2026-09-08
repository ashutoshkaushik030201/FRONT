import { apiClient } from '@/shared/lib/api-client'
import type { User } from '@/domain/types/user'
import type { PaginatedResponse } from '@/domain/types/asset'

export async function listUsers(page = 1, pageSize = 100): Promise<PaginatedResponse<User>> {
  const { data } = await apiClient.get<PaginatedResponse<User>>('/users', {
    params: { page, page_size: pageSize },
  })
  return data
}
