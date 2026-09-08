import { Badge } from '@/shared/components/ui/badge'
import type { AssetStatus } from '@/domain/types/asset'

const STATUS_CONFIG: Record<AssetStatus, { label: string; variant: 'success' | 'warning' | 'secondary' | 'destructive' }> = {
  active: { label: 'Active', variant: 'success' },
  in_repair: { label: 'In Repair', variant: 'warning' },
  retired: { label: 'Retired', variant: 'secondary' },
  disposed: { label: 'Disposed', variant: 'destructive' },
}

export function AssetStatusBadge({ status }: { status: AssetStatus }) {
  const config = STATUS_CONFIG[status]
  return <Badge variant={config.variant}>{config.label}</Badge>
}
