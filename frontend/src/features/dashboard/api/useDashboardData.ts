import { useQuery } from '@tanstack/react-query'

import { listAssetCategories } from '@/features/assets/api/asset-categories.api'
import { listAssets } from '@/features/assets/api/assets.api'

const DASHBOARD_SAMPLE_SIZE = 100

/**
 * The backend does not (yet) expose a dedicated aggregation endpoint, so the dashboard
 * approximates distribution charts client-side from the first page of assets. This is a
 * reasonable trade-off for the current (seed-scale) data volume.
 */
export function useDashboardData() {
  const assetsQuery = useQuery({
    queryKey: ['dashboard', 'assets-sample'],
    queryFn: () => listAssets({ page: 1, page_size: DASHBOARD_SAMPLE_SIZE }),
    staleTime: 60_000,
  })

  const categoriesQuery = useQuery({
    queryKey: ['asset-categories'],
    queryFn: listAssetCategories,
    staleTime: 5 * 60_000,
  })

  return {
    assets: assetsQuery.data?.items ?? [],
    total: assetsQuery.data?.total ?? 0,
    categories: categoriesQuery.data ?? [],
    isLoading: assetsQuery.isLoading || categoriesQuery.isLoading,
  }
}
