import { useMutation, useQueryClient } from '@tanstack/react-query'

import { assignAsset } from '@/features/assets/api/assets.api'
import type { AssignAssetFormValues } from '@/domain/schemas/asset.schema'

export function useAssignAsset(assetId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (payload: AssignAssetFormValues) => assignAsset(assetId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assets'] })
    },
  })
}
