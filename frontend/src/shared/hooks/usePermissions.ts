import { useMemo } from 'react'

import { useAuthStore } from '@/features/auth/store/auth.store'
import type { UserRole } from '@/domain/types/user'

const WRITE_ROLES: UserRole[] = ['admin', 'manager']

export function usePermissions() {
  const user = useAuthStore((state) => state.user)

  return useMemo(() => {
    const role = user?.role ?? null

    return {
      role,
      isAdmin: role === 'admin',
      isManager: role === 'manager',
      isViewer: role === 'viewer',
      /** True for roles allowed to create/update assets and manage assignments. */
      canWrite: role !== null && WRITE_ROLES.includes(role),
      /** True only for roles allowed to manage users/registration. */
      canManageUsers: role === 'admin',
      hasRole: (...roles: UserRole[]) => role !== null && roles.includes(role),
    }
  }, [user])
}
