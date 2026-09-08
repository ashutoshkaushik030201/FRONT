import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'

import { AssetDataGrid } from '@/features/assets/components/AssetDataGrid'
import type { Asset } from '@/domain/types/asset'

vi.mock('@/shared/hooks/usePermissions', () => ({
  usePermissions: () => ({ canWrite: true }),
}))

const assets: Asset[] = [
  {
    id: 'a1',
    asset_tag: 'HW-0001',
    name: 'Dell Latitude 5540',
    description: null,
    category_id: 'cat-1',
    status: 'active',
    assigned_to_user_id: null,
    purchase_cost: '1450.00',
    purchase_date: '2024-01-15',
    salvage_value: '150.00',
    useful_life_months: 36,
    depreciation_method: 'straight_line',
    metadata: {},
    created_at: '2024-01-15T00:00:00Z',
    updated_at: '2024-01-15T00:00:00Z',
  },
  {
    id: 'a2',
    asset_tag: 'HW-0002',
    name: 'PowerEdge R750',
    description: null,
    category_id: 'cat-2',
    status: 'retired',
    assigned_to_user_id: null,
    purchase_cost: '8200.00',
    purchase_date: '2022-05-01',
    salvage_value: '500.00',
    useful_life_months: 60,
    depreciation_method: 'declining_balance',
    metadata: {},
    created_at: '2022-05-01T00:00:00Z',
    updated_at: '2022-05-01T00:00:00Z',
  },
]

describe('AssetDataGrid', () => {
  it('renders asset rows with status badges', () => {
    render(
      <AssetDataGrid
        assets={assets}
        isLoading={false}
        sortBy="created_at"
        sortOrder="desc"
        onSortChange={vi.fn()}
        onView={vi.fn()}
        onAssign={vi.fn()}
      />,
    )

    expect(screen.getByText('Dell Latitude 5540')).toBeInTheDocument()
    expect(screen.getByText('Active')).toBeInTheDocument()
    expect(screen.getByText('Retired')).toBeInTheDocument()
  })

  it('shows a loading skeleton state', () => {
    render(
      <AssetDataGrid
        assets={undefined}
        isLoading
        sortBy={undefined}
        sortOrder="asc"
        onSortChange={vi.fn()}
        onView={vi.fn()}
        onAssign={vi.fn()}
      />,
    )

    expect(screen.queryByText('Dell Latitude 5540')).not.toBeInTheDocument()
  })

  it('shows an empty state when there are no assets', () => {
    render(
      <AssetDataGrid
        assets={[]}
        isLoading={false}
        sortBy={undefined}
        sortOrder="asc"
        onSortChange={vi.fn()}
        onView={vi.fn()}
        onAssign={vi.fn()}
      />,
    )

    expect(screen.getByText(/no assets match the current filters/i)).toBeInTheDocument()
  })

  it('invokes onSortChange when a sortable header is clicked', async () => {
    const user = userEvent.setup()
    const onSortChange = vi.fn()

    render(
      <AssetDataGrid
        assets={assets}
        isLoading={false}
        sortBy="created_at"
        sortOrder="desc"
        onSortChange={onSortChange}
        onView={vi.fn()}
        onAssign={vi.fn()}
      />,
    )

    await user.click(screen.getByRole('button', { name: /name/i }))
    expect(onSortChange).toHaveBeenCalledWith('name')
  })

  it('invokes onView when a row is clicked', async () => {
    const user = userEvent.setup()
    const onView = vi.fn()

    render(
      <AssetDataGrid
        assets={assets}
        isLoading={false}
        sortBy="created_at"
        sortOrder="desc"
        onSortChange={vi.fn()}
        onView={onView}
        onAssign={vi.fn()}
      />,
    )

    await user.click(screen.getByText('Dell Latitude 5540'))
    expect(onView).toHaveBeenCalledWith(assets[0])
  })
})
