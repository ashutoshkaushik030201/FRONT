import { useState } from 'react'
import { Plus } from 'lucide-react'

import { AssetAssignDialog } from '@/features/assets/components/AssetAssignDialog'
import { AssetDataGrid } from '@/features/assets/components/AssetDataGrid'
import { AssetDetailsSheet } from '@/features/assets/components/AssetDetailsSheet'
import { AssetFilters } from '@/features/assets/components/AssetFilters'
import { AssetFormSheet } from '@/features/assets/components/AssetFormSheet'
import { useAssets } from '@/features/assets/api/useAssets'
import { Button } from '@/shared/components/ui/button'
import { DataTablePagination } from '@/shared/components/DataTablePagination'
import { usePermissions } from '@/shared/hooks/usePermissions'
import type { Asset, AssetStatus } from '@/domain/types/asset'

const PAGE_SIZE = 10

export function AssetsPage() {
  const { canWrite } = usePermissions()

  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [categoryId, setCategoryId] = useState<string | undefined>(undefined)
  const [status, setStatus] = useState<AssetStatus | undefined>(undefined)
  const [sortBy, setSortBy] = useState<string | undefined>('created_at')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc')

  const [selectedAsset, setSelectedAsset] = useState<Asset | null>(null)
  const [detailsOpen, setDetailsOpen] = useState(false)
  const [formOpen, setFormOpen] = useState(false)
  const [formAsset, setFormAsset] = useState<Asset | null>(null)
  const [assignAsset, setAssignAsset] = useState<Asset | null>(null)
  const [assignOpen, setAssignOpen] = useState(false)

  const { data, isLoading, isFetching } = useAssets({
    page,
    page_size: PAGE_SIZE,
    search: search || undefined,
    category_id: categoryId,
    status,
    sort_by: sortBy,
    sort_order: sortOrder,
  })

  const handleSortChange = (column: string) => {
    if (sortBy === column) {
      setSortOrder((prev) => (prev === 'asc' ? 'desc' : 'asc'))
    } else {
      setSortBy(column)
      setSortOrder('asc')
    }
    setPage(1)
  }

  const handleSearchChange = (value: string) => {
    setSearch(value)
    setPage(1)
  }

  const handleView = (asset: Asset) => {
    setSelectedAsset(asset)
    setDetailsOpen(true)
  }

  const handleEdit = (asset: Asset) => {
    setDetailsOpen(false)
    setFormAsset(asset)
    setFormOpen(true)
  }

  const handleAssign = (asset: Asset) => {
    setAssignAsset(asset)
    setAssignOpen(true)
  }

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Assets</h1>
          <p className="text-muted-foreground text-sm">Manage hardware and software license inventory.</p>
        </div>
        {canWrite ? (
          <Button
            onClick={() => {
              setFormAsset(null)
              setFormOpen(true)
            }}
          >
            <Plus className="size-4" />
            New Asset
          </Button>
        ) : null}
      </div>

      <AssetFilters
        search={search}
        onSearchChange={handleSearchChange}
        categoryId={categoryId}
        onCategoryChange={(value) => {
          setCategoryId(value)
          setPage(1)
        }}
        status={status}
        onStatusChange={(value) => {
          setStatus(value)
          setPage(1)
        }}
      />

      <AssetDataGrid
        assets={data?.items}
        isLoading={isLoading || isFetching}
        sortBy={sortBy}
        sortOrder={sortOrder}
        onSortChange={handleSortChange}
        onView={handleView}
        onAssign={handleAssign}
      />

      {data ? (
        <DataTablePagination
          page={data.page}
          totalPages={data.total_pages}
          total={data.total}
          pageSize={data.page_size}
          onPageChange={setPage}
        />
      ) : null}

      <AssetDetailsSheet asset={selectedAsset} open={detailsOpen} onOpenChange={setDetailsOpen} onEdit={handleEdit} />
      <AssetFormSheet open={formOpen} onOpenChange={setFormOpen} asset={formAsset} />
      <AssetAssignDialog asset={assignAsset} open={assignOpen} onOpenChange={setAssignOpen} />
    </div>
  )
}
