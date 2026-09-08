import { LayoutDashboard, Package } from 'lucide-react'
import { NavLink, Outlet } from 'react-router-dom'

import { NotificationBell } from '@/features/notifications/components/NotificationBell'
import { ExportButton } from '@/features/reports/components/ExportButton'
import { UserMenu } from '@/shared/components/UserMenu'
import { cn } from '@/shared/lib/utils'

const NAV_ITEMS = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard, end: true },
  { to: '/assets', label: 'Assets', icon: Package, end: false },
]

export function AppShell() {
  return (
    <div className="flex min-h-svh flex-col lg:flex-row">
      <aside className="bg-card flex flex-col gap-1 border-b p-4 lg:w-56 lg:border-b-0 lg:border-r">
        <div className="mb-4 px-2 text-lg font-bold tracking-tight">Nexus</div>
        <nav className="flex flex-row gap-1 lg:flex-col">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-primary text-primary-foreground'
                    : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground',
                )
              }
            >
              <item.icon className="size-4" />
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>

      <div className="flex flex-1 flex-col">
        <header className="bg-background/80 sticky top-0 z-20 flex items-center justify-end gap-2 border-b px-4 py-3 backdrop-blur">
          <ExportButton />
          <NotificationBell />
          <UserMenu />
        </header>

        <main className="flex-1 p-4 lg:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
