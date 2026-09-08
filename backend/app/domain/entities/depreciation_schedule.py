from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID


@dataclass
class DepreciationSchedule:
    id: UUID | None
    asset_id: UUID
    period_start: date
    period_end: date
    opening_book_value: Decimal
    depreciation_amount: Decimal
    closing_book_value: Decimal
    created_at: datetime | None = None
