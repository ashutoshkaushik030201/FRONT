import uuid
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from app.domain.entities.asset import Asset, AssetStatus
from app.domain.exceptions import EntityNotFoundError
from app.domain.repositories.asset_repository import AssetRepository
from app.domain.value_objects.depreciation_method import DepreciationMethod

_UPDATABLE_FIELDS = (
    "name",
    "description",
    "category_id",
    "status",
    "purchase_cost",
    "purchase_date",
    "salvage_value",
    "useful_life_months",
    "depreciation_method",
    "metadata",
)


@dataclass
class UpdateAssetInput:
    name: str | None = None
    description: str | None = None
    category_id: uuid.UUID | None = None
    status: AssetStatus | None = None
    purchase_cost: Decimal | None = None
    purchase_date: date | None = None
    salvage_value: Decimal | None = None
    useful_life_months: int | None = None
    depreciation_method: DepreciationMethod | None = None
    metadata: dict | None = None


class UpdateAssetUseCase:
    def __init__(self, asset_repository: AssetRepository) -> None:
        self._asset_repository = asset_repository

    async def execute(self, asset_id: uuid.UUID, data: UpdateAssetInput) -> Asset:
        asset = await self._asset_repository.get_by_id(asset_id)
        if asset is None or asset.is_deleted:
            raise EntityNotFoundError("Asset", asset_id)

        for field_name in _UPDATABLE_FIELDS:
            value = getattr(data, field_name)
            if value is not None:
                setattr(asset, field_name, value)

        return await self._asset_repository.update(asset)
