import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { toast } from 'sonner'

import { useAssignAsset } from '@/features/assets/api/useAssignAsset'
import { useUsers } from '@/features/users/api/useUsers'
import { Button } from '@/shared/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/shared/components/ui/dialog'
import { Label } from '@/shared/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/shared/components/ui/select'
import { Textarea } from '@/shared/components/ui/textarea'
import { extractErrorMessage } from '@/shared/lib/api-client'
import { assignAssetSchema, type AssignAssetFormValues } from '@/domain/schemas/asset.schema'
import type { Asset } from '@/domain/types/asset'

interface AssetAssignDialogProps {
  asset: Asset | null
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function AssetAssignDialog({ asset, open, onOpenChange }: AssetAssignDialogProps) {
  const { data: usersPage } = useUsers()
  const assignAsset = useAssignAsset(asset?.id ?? '')

  const {
    handleSubmit,
    register,
    watch,
    setValue,
    reset,
    formState: { errors },
  } = useForm<AssignAssetFormValues>({
    resolver: zodResolver(assignAssetSchema),
    defaultValues: { user_id: '', notes: '' },
  })

  const userId = watch('user_id')

  const onSubmit = handleSubmit(async (values) => {
    try {
      await assignAsset.mutateAsync(values)
      toast.success(`Assigned ${asset?.name} successfully`)
      reset({ user_id: '', notes: '' })
      onOpenChange(false)
    } catch (error) {
      toast.error(extractErrorMessage(error, 'Unable to assign asset'))
    }
  })

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Assign Asset</DialogTitle>
          <DialogDescription>
            Assign <span className="font-medium">{asset?.name}</span> to a user. Any existing assignment will be
            closed automatically.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={onSubmit} className="flex flex-col gap-4">
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="assign_user">User</Label>
            <Select value={userId} onValueChange={(value) => setValue('user_id', value, { shouldValidate: true })}>
              <SelectTrigger id="assign_user" className="w-full">
                <SelectValue placeholder="Select a user" />
              </SelectTrigger>
              <SelectContent>
                {usersPage?.items.map((user) => (
                  <SelectItem key={user.id} value={user.id}>
                    {user.full_name} ({user.email})
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {errors.user_id ? <p className="text-destructive text-sm">{errors.user_id.message}</p> : null}
          </div>

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="assign_notes">Notes (optional)</Label>
            <Textarea id="assign_notes" rows={3} placeholder="Reason for assignment…" {...register('notes')} />
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={assignAsset.isPending}>
              {assignAsset.isPending ? 'Assigning…' : 'Assign'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
