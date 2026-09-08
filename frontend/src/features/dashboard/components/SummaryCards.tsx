import { Card, CardContent, CardHeader, CardTitle } from '@/shared/components/ui/card'
import { Skeleton } from '@/shared/components/ui/skeleton'
import type { Asset } from '@/domain/types/asset'

interface SummaryCardsProps {
  assets: Asset[]
  total: number
  isLoading: boolean
}

function formatCurrency(value: number): string {
  return value.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 })
}

export function SummaryCards({ assets, total, isLoading }: SummaryCardsProps) {
  const activeCount = assets.filter((asset) => asset.status === 'active').length
  const maintenanceCount = assets.filter((asset) => asset.status === 'in_repair').length
  const totalValue = assets.reduce((sum, asset) => sum + Number(asset.purchase_cost), 0)

  const cards = [
    { label: 'Total Assets', value: total.toLocaleString() },
    { label: 'Active', value: activeCount.toLocaleString() },
    { label: 'In Repair', value: maintenanceCount.toLocaleString() },
    { label: 'Total Purchase Value', value: formatCurrency(totalValue) },
  ]

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {cards.map((card) => (
        <Card key={card.label}>
          <CardHeader className="pb-2">
            <CardTitle className="text-muted-foreground text-sm font-medium">{card.label}</CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? <Skeleton className="h-8 w-24" /> : <p className="text-2xl font-semibold">{card.value}</p>}
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
