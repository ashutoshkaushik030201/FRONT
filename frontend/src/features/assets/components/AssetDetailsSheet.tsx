import { useState } from 'react'
import { toast } from 'sonner'

import { AssetStatusBadge } from '@/features/assets/components/AssetStatusBadge'
import { useDepreciationSchedule } from '@/features/assets/api/useDepreciationSchedule'
import { useRecalculateDepreciation } from '@/features/assets/api/useRecalculateDepreciation'
import { Button } from '@/shared/components/ui/button'
import { Separator } from '@/shared/components/ui/separator'
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
} from '@/shared/components/ui/sheet'
import { Skeleton } from '@/shared/components/ui/skeleton'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/shared/components/ui/table'
import { usePermissions } from '@/shared/hooks/usePermissions'
import { extractErrorMessage } from '@/shared/lib/api-client'
import type { Asset } from '@/domain/types/asset'

interface AssetDetailsSheetProps {
  asset: Asset | null
  open: boolean
  onOpenChange: (open: boolean) => void
  onEdit: (asset: Asset) => void
}

function formatMoney(value: string): string {
  const amount = Number(value)
  return Number.isFinite(amount) ? amount.toLocaleString('en-US', { style: 'currency', currency: 'USD' }) : value
}

export function AssetDetailsSheet({ asset, open, onOpenChange, onEdit }: AssetDetailsSheetProps) {
  const { canWrite } = usePermissions()
  const [showSchedule, setShowSchedule] = useState(false)
  const { data: schedule, isLoading: isScheduleLoading } = useDepreciationSchedule(showSchedule ? (asset?.id ?? null) : null)
  const recalculate = useRecalculateDepreciation(asset?.id ?? '')

  if (!asset) return null

  const handleRecalculate = async () => {
    try {
      await recalculate.mutateAsync()
      setShowSchedule(true)
      toast.success('Depreciation schedule recalculated')
    } catch (error) {
      toast.error(extractErrorMessage(error, 'Unable to recalculate depreciation'))
    }
  }

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent className="overflow-y-auto sm:max-w-xl">
        <SheetHeader>
          <SheetTitle className="flex items-center gap-2">
            {asset.name}
            <AssetStatusBadge status={asset.status} />
          </SheetTitle>
          <SheetDescription>{asset.asset_tag}</SheetDescription>
        </SheetHeader>

        <div className="flex flex-col gap-4 px-4 pb-4">
          {asset.description ? <p className="text-sm">{asset.description}</p> : null}

          <dl className="grid grid-cols-2 gap-3 text-sm">
            <div>
              <dt className="text-muted-foreground">Purchase Cost</dt>
              <dd className="font-medium">{formatMoney(asset.purchase_cost)}</dd>
            </div>
            <div>
              <dt className="text-muted-foreground">Salvage Value</dt>
              <dd className="font-medium">{formatMoney(asset.salvage_value)}</dd>
            </div>
            <div>
              <dt className="text-muted-foreground">Purchase Date</dt>
              <dd className="font-medium">{new Date(asset.purchase_date).toLocaleDateString()}</dd>
            </div>
            <div>
              <dt className="text-muted-foreground">Useful Life</dt>
              <dd className="font-medium">{asset.useful_life_months} months</dd>
            </div>
            <div>
              <dt className="text-muted-foreground">Depreciation Method</dt>
              <dd className="font-medium capitalize">{asset.depreciation_method.replace('_', ' ')}</dd>
            </div>
          </dl>

          <Separator />

          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold">Depreciation Schedule</h3>
            <div className="flex gap-2">
              <Button size="sm" variant="outline" onClick={() => setShowSchedule((prev) => !prev)}>
                {showSchedule ? 'Hide' : 'Preview'}
              </Button>
              {canWrite ? (
                <Button size="sm" variant="outline" onClick={handleRecalculate} disabled={recalculate.isPending}>
                  {recalculate.isPending ? 'Calculating…' : 'Recalculate'}
                </Button>
              ) : null}
            </div>
          </div>

          {showSchedule ? (
            <div className="max-h-64 overflow-y-auto rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Period</TableHead>
                    <TableHead>Opening</TableHead>
                    <TableHead>Depreciation</TableHead>
                    <TableHead>Closing</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {isScheduleLoading
                    ? Array.from({ length: 4 }).map((_, index) => (
                        <TableRow key={`schedule-skeleton-${index}`}>
                          <TableCell colSpan={4}>
                            <Skeleton className="h-4 w-full" />
                          </TableCell>
                        </TableRow>
                      ))
                    : null}
                  {!isScheduleLoading && schedule?.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={4} className="text-muted-foreground text-center">
                        No schedule yet — click Recalculate.
                      </TableCell>
                    </TableRow>
                  ) : null}
                  {!isScheduleLoading &&
                    schedule?.map((entry) => (
                      <TableRow key={entry.id}>
                        <TableCell className="whitespace-nowrap">
                          {new Date(entry.period_start).toLocaleDateString()} –{' '}
                          {new Date(entry.period_end).toLocaleDateString()}
                        </TableCell>
                        <TableCell>{formatMoney(entry.opening_book_value)}</TableCell>
                        <TableCell>{formatMoney(entry.depreciation_amount)}</TableCell>
                        <TableCell>{formatMoney(entry.closing_book_value)}</TableCell>
                      </TableRow>
                    ))}
                </TableBody>
              </Table>
            </div>
          ) : null}
        </div>

        {canWrite ? (
          <SheetFooter className="flex-row justify-end gap-2">
            <Button variant="outline" onClick={() => onEdit(asset)}>
              Edit Asset
            </Button>
          </SheetFooter>
        ) : null}
      </SheetContent>
    </Sheet>
  )
}
