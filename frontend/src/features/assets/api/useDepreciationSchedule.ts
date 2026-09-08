import { useQuery } from '@tanstack/react-query'

import { getDepreciationSchedule } from '@/features/assets/api/assets.api'

export function useDepreciationSchedule(assetId: string | null) {
  return useQuery({
    queryKey: ['assets', assetId, 'depreciation'],
    queryFn: () => getDepreciationSchedule(assetId as string),
    enabled: Boolean(assetId),
  })
}
