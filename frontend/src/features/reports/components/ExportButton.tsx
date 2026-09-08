import { Download } from 'lucide-react'

import { Button } from '@/shared/components/ui/button'
import { Tooltip, TooltipContent, TooltipTrigger } from '@/shared/components/ui/tooltip'

/** Stub for the future Celery/Redis-backed PDF/Excel export engine (not implemented yet). */
export function ExportButton() {
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <span>
          <Button variant="outline" size="sm" disabled aria-label="Export report (coming soon)">
            <Download className="size-4" />
            Export
          </Button>
        </span>
      </TooltipTrigger>
      <TooltipContent>Report export — coming soon</TooltipContent>
    </Tooltip>
  )
}
