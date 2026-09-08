from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class AssetAssignment:
    id: UUID | None
    asset_id: UUID
    user_id: UUID
    assigned_at: datetime
    returned_at: datetime | None = None
    notes: str | None = None
