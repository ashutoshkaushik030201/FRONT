export type AssetStatus = 'active' | 'in_repair' | 'retired' | 'disposed'
export type DepreciationMethod = 'straight_line' | 'declining_balance'

export interface AssetCategory {
  id: string
  name: string
  type: 'hardware' | 'software_license'
}

export interface Asset {
  id: string
  asset_tag: string
  name: string
  description: string | null
  category_id: string
  status: AssetStatus
  assigned_to_user_id: string | null
  purchase_cost: string
  purchase_date: string
  salvage_value: string
  useful_life_months: number
  depreciation_method: DepreciationMethod
  metadata: Record<string, unknown>
  created_at: string
  updated_at: string
}

export interface AssetAssignment {
  id: string
  asset_id: string
  user_id: string
  assigned_at: string
  returned_at: string | null
  notes: string | null
}

export interface DepreciationScheduleEntry {
  id: string
  asset_id: string
  period_start: string
  period_end: string
  opening_book_value: string
  depreciation_amount: string
  closing_book_value: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface AssetListParams {
  page?: number
  page_size?: number
  search?: string
  category_id?: string
  status?: AssetStatus
  sort_by?: string
  sort_order?: 'asc' | 'desc'
}
