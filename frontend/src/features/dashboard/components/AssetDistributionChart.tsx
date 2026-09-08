import { Bar, BarChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

import { Card, CardContent, CardHeader, CardTitle } from '@/shared/components/ui/card'
import { Skeleton } from '@/shared/components/ui/skeleton'
import type { Asset, AssetCategory, AssetStatus } from '@/domain/types/asset'

const STATUS_COLORS: Record<AssetStatus, string> = {
  active: 'var(--color-success, #22c55e)',
  in_repair: 'var(--color-warning, #eab308)',
  retired: 'var(--color-muted-foreground, #a1a1aa)',
  disposed: 'var(--color-destructive, #ef4444)',
}

const STATUS_LABELS: Record<AssetStatus, string> = {
  active: 'Active',
  in_repair: 'In Repair',
  retired: 'Retired',
  disposed: 'Disposed',
}

interface AssetDistributionChartProps {
  assets: Asset[]
  categories: AssetCategory[]
  isLoading: boolean
}

export function AssetDistributionChart({ assets, categories, isLoading }: AssetDistributionChartProps) {
  const statusData = (Object.keys(STATUS_LABELS) as AssetStatus[])
    .map((status) => ({
      status,
      label: STATUS_LABELS[status],
      value: assets.filter((asset) => asset.status === status).length,
    }))
    .filter((entry) => entry.value > 0)

  const categoryData = categories
    .map((category) => ({
      name: category.name,
      value: assets.filter((asset) => asset.category_id === category.id).length,
    }))
    .filter((entry) => entry.value > 0)

  if (isLoading) {
    return (
      <div className="grid gap-4 lg:grid-cols-2">
        <Skeleton className="h-72 w-full" />
        <Skeleton className="h-72 w-full" />
      </div>
    )
  }

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Assets by Status</CardTitle>
        </CardHeader>
        <CardContent className="h-64">
          {statusData.length === 0 ? (
            <EmptyState />
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={statusData} dataKey="value" nameKey="label" innerRadius={50} outerRadius={80} paddingAngle={2}>
                  {statusData.map((entry) => (
                    <Cell key={entry.status} fill={STATUS_COLORS[entry.status]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Assets by Category</CardTitle>
        </CardHeader>
        <CardContent className="h-64">
          {categoryData.length === 0 ? (
            <EmptyState />
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={categoryData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" tick={{ fontSize: 12 }} interval={0} angle={-15} textAnchor="end" height={50} />
                <YAxis allowDecimals={false} tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="value" fill="var(--color-primary, #171717)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

function EmptyState() {
  return <div className="text-muted-foreground flex h-full items-center justify-center text-sm">No data yet</div>
}
