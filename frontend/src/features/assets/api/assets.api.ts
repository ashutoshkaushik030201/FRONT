import { apiClient } from '@/shared/lib/api-client'
import type {
  Asset,
  AssetAssignment,
  AssetListParams,
  DepreciationScheduleEntry,
  PaginatedResponse,
} from '@/domain/types/asset'
import type { AssetFormValues, AssignAssetFormValues } from '@/domain/schemas/asset.schema'

export async function listAssets(params: AssetListParams): Promise<PaginatedResponse<Asset>> {
  const { data } = await apiClient.get<PaginatedResponse<Asset>>('/assets', { params })
  return data
}

export async function getAsset(assetId: string): Promise<Asset> {
  const { data } = await apiClient.get<Asset>(`/assets/${assetId}`)
  return data
}

export async function createAsset(payload: AssetFormValues): Promise<Asset> {
  const { data } = await apiClient.post<Asset>('/assets', payload)
  return data
}

export async function updateAsset(assetId: string, payload: Partial<AssetFormValues>): Promise<Asset> {
  const { data } = await apiClient.patch<Asset>(`/assets/${assetId}`, payload)
  return data
}

export async function assignAsset(assetId: string, payload: AssignAssetFormValues): Promise<AssetAssignment> {
  const { data } = await apiClient.post<AssetAssignment>(`/assets/${assetId}/assign`, payload)
  return data
}

export async function getDepreciationSchedule(assetId: string): Promise<DepreciationScheduleEntry[]> {
  const { data } = await apiClient.get<DepreciationScheduleEntry[]>(`/assets/${assetId}/depreciation`)
  return data
}

export async function recalculateDepreciation(assetId: string): Promise<DepreciationScheduleEntry[]> {
  const { data } = await apiClient.post<DepreciationScheduleEntry[]>(`/assets/${assetId}/depreciation/recalculate`)
  return data
}
