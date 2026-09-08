import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.domain.entities.asset import AssetStatus
from app.domain.value_objects.depreciation_method import DepreciationMethod


class AssetCreateRequest(BaseModel):
    asset_tag: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    category_id: uuid.UUID
    purchase_cost: Decimal = Field(gt=0)
    purchase_date: date
    salvage_value: Decimal = Field(ge=0)
    useful_life_months: int = Field(gt=0)
    depreciation_method: DepreciationMethod = DepreciationMethod.STRAIGHT_LINE
    metadata: dict = Field(default_factory=dict)


class AssetUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    category_id: uuid.UUID | None = None
    status: AssetStatus | None = None
    purchase_cost: Decimal | None = Field(default=None, gt=0)
    purchase_date: date | None = None
    salvage_value: Decimal | None = Field(default=None, ge=0)
    useful_life_months: int | None = Field(default=None, gt=0)
    depreciation_method: DepreciationMethod | None = None
    metadata: dict | None = None


class AssetResponse(BaseModel):
    id: uuid.UUID
    asset_tag: str
    name: str
    description: str | None
    category_id: uuid.UUID
    status: AssetStatus
    assigned_to_user_id: uuid.UUID | None
    purchase_cost: Decimal
    purchase_date: date
    salvage_value: Decimal
    useful_life_months: int
    depreciation_method: DepreciationMethod
    metadata: dict
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AssetAssignRequest(BaseModel):
    user_id: uuid.UUID
    notes: str | None = None


class AssetAssignmentResponse(BaseModel):
    id: uuid.UUID
    asset_id: uuid.UUID
    user_id: uuid.UUID
    assigned_at: datetime
    returned_at: datetime | None
    notes: str | None

    model_config = {"from_attributes": True}


class DepreciationScheduleResponse(BaseModel):
    id: uuid.UUID
    asset_id: uuid.UUID
    period_start: date
    period_end: date
    opening_book_value: Decimal
    depreciation_amount: Decimal
    closing_book_value: Decimal

    model_config = {"from_attributes": True}
