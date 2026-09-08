import { useQuery } from '@tanstack/react-query'

import { getAsset } from '@/features/assets/api/assets.api'

export function useAsset(assetId: string | null) {
  return useQuery({
    queryKey: ['assets', assetId],
    queryFn: () => getAsset(assetId as string),
    enabled: Boolean(assetId),
  })
}
