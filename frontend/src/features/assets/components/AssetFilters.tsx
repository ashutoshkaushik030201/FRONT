import { Input } from '@/shared/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/shared/components/ui/select'
import { useAssetCategories } from '@/features/assets/api/useAssetCategories'
import type { AssetStatus } from '@/domain/types/asset'

const STATUS_OPTIONS: { value: AssetStatus; label: string }[] = [
  { value: 'active', label: 'Active' },
  { value: 'in_repair', label: 'In Repair' },
  { value: 'retired', label: 'Retired' },
  { value: 'disposed', label: 'Disposed' },
]

interface AssetFiltersProps {
  search: string
  onSearchChange: (value: string) => void
  categoryId: string | undefined
  onCategoryChange: (value: string | undefined) => void
  status: AssetStatus | undefined
  onStatusChange: (value: AssetStatus | undefined) => void
}

const ALL_VALUE = 'all'

export function AssetFilters({
  search,
  onSearchChange,
  categoryId,
  onCategoryChange,
  status,
  onStatusChange,
}: AssetFiltersProps) {
  const { data: categories } = useAssetCategories()

  return (
    <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
      <Input
        placeholder="Search by name, tag, or description…"
        value={search}
        onChange={(event) => onSearchChange(event.target.value)}
        className="sm:max-w-xs"
      />

      <Select
        value={categoryId ?? ALL_VALUE}
        onValueChange={(value) => onCategoryChange(value === ALL_VALUE ? undefined : value)}
      >
        <SelectTrigger className="sm:w-48">
          <SelectValue placeholder="All categories" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value={ALL_VALUE}>All categories</SelectItem>
          {categories?.map((category) => (
            <SelectItem key={category.id} value={category.id}>
              {category.name}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      <Select
        value={status ?? ALL_VALUE}
        onValueChange={(value) => onStatusChange(value === ALL_VALUE ? undefined : (value as AssetStatus))}
      >
        <SelectTrigger className="sm:w-44">
          <SelectValue placeholder="All statuses" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value={ALL_VALUE}>All statuses</SelectItem>
          {STATUS_OPTIONS.map((option) => (
            <SelectItem key={option.value} value={option.value}>
              {option.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  )
}
