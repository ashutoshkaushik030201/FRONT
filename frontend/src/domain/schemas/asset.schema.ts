import { z } from 'zod'

export const assetFormSchema = z.object({
  asset_tag: z.string().min(1, 'Asset tag is required').max(100),
  name: z.string().min(1, 'Name is required').max(255),
  description: z.string().max(2000).optional().or(z.literal('')),
  category_id: z.string().uuid('Select a category'),
  purchase_cost: z.coerce.number().gt(0, 'Must be greater than 0'),
  purchase_date: z.string().min(1, 'Purchase date is required'),
  salvage_value: z.coerce.number().min(0, 'Cannot be negative'),
  useful_life_months: z.coerce.number().int().gt(0, 'Must be greater than 0'),
  depreciation_method: z.enum(['straight_line', 'declining_balance']),
})

export type AssetFormValues = z.infer<typeof assetFormSchema>
export type AssetFormInput = z.input<typeof assetFormSchema>

export const assignAssetSchema = z.object({
  user_id: z.string().uuid('Select a user'),
  notes: z.string().max(500).optional().or(z.literal('')),
})

export type AssignAssetFormValues = z.infer<typeof assignAssetSchema>
