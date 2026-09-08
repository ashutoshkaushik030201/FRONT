import { keepPreviousData, useQuery } from '@tanstack/react-query'

import { listAssets } from '@/features/assets/api/assets.api'
import type { AssetListParams } from '@/domain/types/asset'

export function useAssets(params: AssetListParams) {
  return useQuery({
    queryKey: ['assets', params],
    queryFn: () => listAssets(params),
    placeholderData: keepPreviousData,
  })
}
