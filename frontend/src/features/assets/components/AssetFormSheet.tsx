import { zodResolver } from '@hookform/resolvers/zod'
import { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { toast } from 'sonner'

import { useAssetCategories } from '@/features/assets/api/useAssetCategories'
import { useCreateAsset } from '@/features/assets/api/useCreateAsset'
import { useUpdateAsset } from '@/features/assets/api/useUpdateAsset'
import { Button } from '@/shared/components/ui/button'
import { Input } from '@/shared/components/ui/input'
import { Label } from '@/shared/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/shared/components/ui/select'
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
} from '@/shared/components/ui/sheet'
import { Textarea } from '@/shared/components/ui/textarea'
import { extractErrorMessage } from '@/shared/lib/api-client'
import { assetFormSchema, type AssetFormInput, type AssetFormValues } from '@/domain/schemas/asset.schema'
import type { Asset } from '@/domain/types/asset'

interface AssetFormSheetProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  asset?: Asset | null
}

function toFormValues(asset?: Asset | null): AssetFormInput {
  if (!asset) {
    return {
      asset_tag: '',
      name: '',
      description: '',
      category_id: '',
      purchase_cost: 0,
      purchase_date: new Date().toISOString().slice(0, 10),
      salvage_value: 0,
      useful_life_months: 36,
      depreciation_method: 'straight_line',
    }
  }

  return {
    asset_tag: asset.asset_tag,
    name: asset.name,
    description: asset.description ?? '',
    category_id: asset.category_id,
    purchase_cost: Number(asset.purchase_cost),
    purchase_date: asset.purchase_date,
    salvage_value: Number(asset.salvage_value),
    useful_life_months: asset.useful_life_months,
    depreciation_method: asset.depreciation_method,
  }
}

export function AssetFormSheet({ open, onOpenChange, asset }: AssetFormSheetProps) {
  const isEditMode = Boolean(asset)
  const { data: categories } = useAssetCategories()
  const createAsset = useCreateAsset()
  const updateAsset = useUpdateAsset(asset?.id ?? '')

  const {
    register,
    handleSubmit,
    reset,
    watch,
    setValue,
    formState: { errors },
  } = useForm<AssetFormInput, unknown, AssetFormValues>({
    resolver: zodResolver(assetFormSchema),
    defaultValues: toFormValues(asset),
  })

  useEffect(() => {
    if (open) {
      reset(toFormValues(asset))
    }
  }, [open, asset, reset])

  const isPending = createAsset.isPending || updateAsset.isPending

  const onSubmit = handleSubmit(async (values) => {
    try {
      if (isEditMode && asset) {
        await updateAsset.mutateAsync(values)
        toast.success('Asset updated')
      } else {
        await createAsset.mutateAsync(values)
        toast.success('Asset created')
      }
      onOpenChange(false)
    } catch (error) {
      toast.error(extractErrorMessage(error, 'Unable to save asset'))
    }
  })

  const categoryValue = watch('category_id')
  const depreciationMethodValue = watch('depreciation_method')

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent className="overflow-y-auto">
        <SheetHeader>
          <SheetTitle>{isEditMode ? 'Edit Asset' : 'New Asset'}</SheetTitle>
          <SheetDescription>
            {isEditMode ? 'Update the asset record.' : 'Register a new hardware or software license asset.'}
          </SheetDescription>
        </SheetHeader>

        <form onSubmit={onSubmit} className="flex flex-col gap-4 px-4 pb-4" noValidate>
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="asset_tag">Asset Tag</Label>
            <Input id="asset_tag" {...register('asset_tag')} disabled={isEditMode} />
            {errors.asset_tag ? <p className="text-destructive text-sm">{errors.asset_tag.message}</p> : null}
          </div>

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="name">Name</Label>
            <Input id="name" {...register('name')} />
            {errors.name ? <p className="text-destructive text-sm">{errors.name.message}</p> : null}
          </div>

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="description">Description</Label>
            <Textarea id="description" rows={3} {...register('description')} />
          </div>

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="category_id">Category</Label>
            <Select value={categoryValue} onValueChange={(value) => setValue('category_id', value, { shouldValidate: true })}>
              <SelectTrigger id="category_id" className="w-full">
                <SelectValue placeholder="Select a category" />
              </SelectTrigger>
              <SelectContent>
                {categories?.map((category) => (
                  <SelectItem key={category.id} value={category.id}>
                    {category.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {errors.category_id ? <p className="text-destructive text-sm">{errors.category_id.message}</p> : null}
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="purchase_cost">Purchase Cost</Label>
              <Input id="purchase_cost" type="number" step="0.01" {...register('purchase_cost')} />
              {errors.purchase_cost ? <p className="text-destructive text-sm">{errors.purchase_cost.message}</p> : null}
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="salvage_value">Salvage Value</Label>
              <Input id="salvage_value" type="number" step="0.01" {...register('salvage_value')} />
              {errors.salvage_value ? <p className="text-destructive text-sm">{errors.salvage_value.message}</p> : null}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="purchase_date">Purchase Date</Label>
              <Input id="purchase_date" type="date" {...register('purchase_date')} />
              {errors.purchase_date ? <p className="text-destructive text-sm">{errors.purchase_date.message}</p> : null}
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="useful_life_months">Useful Life (months)</Label>
              <Input id="useful_life_months" type="number" {...register('useful_life_months')} />
              {errors.useful_life_months ? (
                <p className="text-destructive text-sm">{errors.useful_life_months.message}</p>
              ) : null}
            </div>
          </div>

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="depreciation_method">Depreciation Method</Label>
            <Select
              value={depreciationMethodValue}
              onValueChange={(value) =>
                setValue('depreciation_method', value as AssetFormValues['depreciation_method'], {
                  shouldValidate: true,
                })
              }
            >
              <SelectTrigger id="depreciation_method" className="w-full">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="straight_line">Straight Line</SelectItem>
                <SelectItem value="declining_balance">Declining Balance</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <SheetFooter className="mt-2 flex-row justify-end gap-2 p-0">
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={isPending}>
              {isPending ? 'Saving…' : 'Save Asset'}
            </Button>
          </SheetFooter>
        </form>
      </SheetContent>
    </Sheet>
  )
}
