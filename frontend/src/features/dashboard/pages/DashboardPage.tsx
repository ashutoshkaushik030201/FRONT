import { AssetDistributionChart } from '@/features/dashboard/components/AssetDistributionChart'
import { SummaryCards } from '@/features/dashboard/components/SummaryCards'
import { useDashboardData } from '@/features/dashboard/api/useDashboardData'

export function DashboardPage() {
  const { assets, total, categories, isLoading } = useDashboardData()

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground text-sm">Asset distribution and compliance overview.</p>
      </div>

      <SummaryCards assets={assets} total={total} isLoading={isLoading} />
      <AssetDistributionChart assets={assets} categories={categories} isLoading={isLoading} />
    </div>
  )
}
