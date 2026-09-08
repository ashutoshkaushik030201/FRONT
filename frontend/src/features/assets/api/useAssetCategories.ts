import { useQuery } from '@tanstack/react-query'

import { listAssetCategories } from '@/features/assets/api/asset-categories.api'

export function useAssetCategories() {
  return useQuery({
    queryKey: ['asset-categories'],
    queryFn: listAssetCategories,
    staleTime: 5 * 60_000,
  })
}
