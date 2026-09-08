import { useMutation, useQueryClient } from '@tanstack/react-query'

import { recalculateDepreciation } from '@/features/assets/api/assets.api'

export function useRecalculateDepreciation(assetId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: () => recalculateDepreciation(assetId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assets', assetId, 'depreciation'] })
    },
  })
}
