import { ArrowDown, ArrowUp, ArrowUpDown, MoreHorizontal } from 'lucide-react'

import { AssetStatusBadge } from '@/features/assets/components/AssetStatusBadge'
import { Button } from '@/shared/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/shared/components/ui/dropdown-menu'
import { Skeleton } from '@/shared/components/ui/skeleton'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/shared/components/ui/table'
import { usePermissions } from '@/shared/hooks/usePermissions'
import type { Asset } from '@/domain/types/asset'

const SORTABLE_COLUMNS: { key: string; label: string }[] = [
  { key: 'asset_tag', label: 'Asset Tag' },
  { key: 'name', label: 'Name' },
  { key: 'status', label: 'Status' },
  { key: 'purchase_cost', label: 'Purchase Cost' },
  { key: 'purchase_date', label: 'Purchase Date' },
]

interface AssetDataGridProps {
  assets: Asset[] | undefined
  isLoading: boolean
  sortBy: string | undefined
  sortOrder: 'asc' | 'desc'
  onSortChange: (column: string) => void
  onView: (asset: Asset) => void
  onAssign: (asset: Asset) => void
}

function formatCurrency(value: string): string {
  const amount = Number(value)
  return Number.isFinite(amount) ? amount.toLocaleString('en-US', { style: 'currency', currency: 'USD' }) : value
}

export function AssetDataGrid({
  assets,
  isLoading,
  sortBy,
  sortOrder,
  onSortChange,
  onView,
  onAssign,
}: AssetDataGridProps) {
  const { canWrite } = usePermissions()

  return (
    <div className="rounded-lg border">
      <div className="max-h-[65vh] overflow-y-auto">
        <Table>
          <TableHeader>
            <TableRow>
              {SORTABLE_COLUMNS.map((column) => (
                <TableHead key={column.key}>
                  <button
                    type="button"
                    onClick={() => onSortChange(column.key)}
                    className="hover:text-foreground inline-flex items-center gap-1 font-medium"
                  >
                    {column.label}
                    {sortBy === column.key ? (
                      sortOrder === 'asc' ? (
                        <ArrowUp className="size-3.5" />
                      ) : (
                        <ArrowDown className="size-3.5" />
                      )
                    ) : (
                      <ArrowUpDown className="size-3.5 opacity-40" />
                    )}
                  </button>
                </TableHead>
              ))}
              <TableHead className="w-10" />
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading
              ? Array.from({ length: 8 }).map((_, index) => (
                  <TableRow key={`skeleton-${index}`}>
                    {SORTABLE_COLUMNS.map((column) => (
                      <TableCell key={column.key}>
                        <Skeleton className="h-4 w-24" />
                      </TableCell>
                    ))}
                    <TableCell>
                      <Skeleton className="h-4 w-4" />
                    </TableCell>
                  </TableRow>
                ))
              : null}

            {!isLoading && assets?.length === 0 ? (
              <TableRow>
                <TableCell colSpan={SORTABLE_COLUMNS.length + 1} className="text-muted-foreground h-24 text-center">
                  No assets match the current filters.
                </TableCell>
              </TableRow>
            ) : null}

            {!isLoading &&
              assets?.map((asset) => (
                <TableRow key={asset.id} className="cursor-pointer" onClick={() => onView(asset)}>
                  <TableCell className="font-medium">{asset.asset_tag}</TableCell>
                  <TableCell>{asset.name}</TableCell>
                  <TableCell>
                    <AssetStatusBadge status={asset.status} />
                  </TableCell>
                  <TableCell>{formatCurrency(asset.purchase_cost)}</TableCell>
                  <TableCell>{new Date(asset.purchase_date).toLocaleDateString()}</TableCell>
                  <TableCell onClick={(event) => event.stopPropagation()}>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon" aria-label="Row actions">
                          <MoreHorizontal className="size-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem onClick={() => onView(asset)}>View / Edit</DropdownMenuItem>
                        {canWrite ? (
                          <DropdownMenuItem onClick={() => onAssign(asset)}>Assign to user</DropdownMenuItem>
                        ) : null}
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}
