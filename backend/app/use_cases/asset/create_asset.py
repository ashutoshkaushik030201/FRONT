import uuid
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

from app.domain.entities.asset import Asset, AssetStatus
from app.domain.exceptions import DuplicateEntityError
from app.domain.repositories.asset_repository import AssetRepository
from app.domain.value_objects.depreciation_method import DepreciationMethod


@dataclass
class CreateAssetInput:
    asset_tag: str
    name: str
    category_id: uuid.UUID
    purchase_cost: Decimal
    purchase_date: date
    salvage_value: Decimal
    useful_life_months: int
    depreciation_method: DepreciationMethod = DepreciationMethod.STRAIGHT_LINE
    description: str | None = None
    metadata: dict = field(default_factory=dict)


class CreateAssetUseCase:
    def __init__(self, asset_repository: AssetRepository) -> None:
        self._asset_repository = asset_repository

    async def execute(self, data: CreateAssetInput) -> Asset:
        existing = await self._asset_repository.get_by_tag(data.asset_tag)
        if existing is not None:
            raise DuplicateEntityError("Asset", "asset_tag", data.asset_tag)

        asset = Asset(
            id=None,
            asset_tag=data.asset_tag,
            name=data.name,
            category_id=data.category_id,
            status=AssetStatus.ACTIVE,
            purchase_cost=data.purchase_cost,
            purchase_date=data.purchase_date,
            salvage_value=data.salvage_value,
            useful_life_months=data.useful_life_months,
            depreciation_method=data.depreciation_method,
            description=data.description,
            metadata=data.metadata,
        )
        return await self._asset_repository.create(asset)
