import { Bell } from 'lucide-react'

import { Button } from '@/shared/components/ui/button'
import { Tooltip, TooltipContent, TooltipTrigger } from '@/shared/components/ui/tooltip'

/** Stub for the future WebSocket-based real-time notification engine (not implemented yet). */
export function NotificationBell() {
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <span>
          <Button variant="ghost" size="icon" disabled aria-label="Notifications (coming soon)">
            <Bell className="size-4" />
          </Button>
        </span>
      </TooltipTrigger>
      <TooltipContent>Real-time notifications — coming soon</TooltipContent>
    </Tooltip>
  )
}
