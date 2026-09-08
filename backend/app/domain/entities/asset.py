from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from app.domain.value_objects.depreciation_method import DepreciationMethod


class AssetStatus(str, Enum):
    ACTIVE = "active"
    IN_REPAIR = "in_repair"
    RETIRED = "retired"
    DISPOSED = "disposed"


@dataclass
class Asset:
    id: UUID | None
    asset_tag: str
    name: str
    category_id: UUID
    status: AssetStatus
    purchase_cost: Decimal
    purchase_date: date
    salvage_value: Decimal
    useful_life_months: int
    depreciation_method: DepreciationMethod
    description: str | None = None
    assigned_to_user_id: UUID | None = None
    metadata: dict = field(default_factory=dict)
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    @property
    def is_assigned(self) -> bool:
        return self.assigned_to_user_id is not None
