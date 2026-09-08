import { apiClient } from '@/shared/lib/api-client'
import type { AssetCategory } from '@/domain/types/asset'

export async function listAssetCategories(): Promise<AssetCategory[]> {
  const { data } = await apiClient.get<AssetCategory[]>('/asset-categories')
  return data
}
