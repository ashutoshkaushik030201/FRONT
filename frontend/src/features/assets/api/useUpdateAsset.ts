import { useMutation, useQueryClient } from '@tanstack/react-query'

import { updateAsset } from '@/features/assets/api/assets.api'
import type { AssetFormValues } from '@/domain/schemas/asset.schema'

export function useUpdateAsset(assetId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (payload: Partial<AssetFormValues>) => updateAsset(assetId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assets'] })
    },
  })
}
