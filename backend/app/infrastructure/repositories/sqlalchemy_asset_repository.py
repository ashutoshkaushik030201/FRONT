import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.asset import Asset, AssetStatus
from app.domain.repositories.asset_repository import AssetRepository
from app.domain.value_objects.depreciation_method import DepreciationMethod
from app.infrastructure.db.models.asset_model import AssetModel

_SORTABLE_COLUMNS = {
    "name": AssetModel.name,
    "asset_tag": AssetModel.asset_tag,
    "purchase_date": AssetModel.purchase_date,
    "purchase_cost": AssetModel.purchase_cost,
    "created_at": AssetModel.created_at,
    "status": AssetModel.status,
}


class SqlAlchemyAssetRepository(AssetRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, asset_id: uuid.UUID) -> Asset | None:
        model = await self._session.get(AssetModel, asset_id)
        return _to_entity(model) if model else None

    async def get_by_tag(self, asset_tag: str) -> Asset | None:
        stmt = select(AssetModel).where(AssetModel.asset_tag == asset_tag)
        model = (await self._session.execute(stmt)).scalar_one_or_none()
        return _to_entity(model) if model else None

    async def list(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        category_id: uuid.UUID | None = None,
        status: str | None = None,
        sort_by: str | None = None,
        sort_order: str = "asc",
    ) -> tuple[list[Asset], int]:
        conditions = [AssetModel.deleted_at.is_(None)]
        if category_id is not None:
            conditions.append(AssetModel.category_id == category_id)
        if status is not None:
            conditions.append(AssetModel.status == status)
        if search:
            conditions.append(AssetModel.search_vector.op("@@")(func.plainto_tsquery("english", search)))

        total = (
            await self._session.execute(select(func.count()).select_from(AssetModel).where(*conditions))
        ).scalar_one()

        stmt = select(AssetModel).where(*conditions)
        sort_column = _SORTABLE_COLUMNS.get(sort_by or "created_at", AssetModel.created_at)
        stmt = stmt.order_by(sort_column.desc() if sort_order == "desc" else sort_column.asc())
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)

        models = (await self._session.execute(stmt)).scalars().all()
        return [_to_entity(model) for model in models], total

    async def create(self, asset: Asset) -> Asset:
        model = AssetModel(
            asset_tag=asset.asset_tag,
            name=asset.name,
            description=asset.description,
            category_id=asset.category_id,
            status=asset.status.value,
            purchase_cost=asset.purchase_cost,
            purchase_date=asset.purchase_date,
            salvage_value=asset.salvage_value,
            useful_life_months=asset.useful_life_months,
            depreciation_method=asset.depreciation_method.value,
            asset_metadata=asset.metadata,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def update(self, asset: Asset) -> Asset:
        model = await self._session.get(AssetModel, asset.id)
        if model is None:
            raise ValueError(f"Asset {asset.id} does not exist")
        model.name = asset.name
        model.description = asset.description
        model.category_id = asset.category_id
        model.status = asset.status.value if isinstance(asset.status, AssetStatus) else asset.status
        model.assigned_to_user_id = asset.assigned_to_user_id
        model.purchase_cost = asset.purchase_cost
        model.purchase_date = asset.purchase_date
        model.salvage_value = asset.salvage_value
        model.useful_life_months = asset.useful_life_months
        method = asset.depreciation_method
        model.depreciation_method = method.value if isinstance(method, DepreciationMethod) else method
        model.asset_metadata = asset.metadata
        await self._session.flush()
        return _to_entity(model)

    async def soft_delete(self, asset_id: uuid.UUID) -> None:
        model = await self._session.get(AssetModel, asset_id)
        if model is not None:
            model.deleted_at = datetime.now(timezone.utc)
            await self._session.flush()


def _to_entity(model: AssetModel) -> Asset:
    return Asset(
        id=model.id,
        asset_tag=model.asset_tag,
        name=model.name,
        category_id=model.category_id,
        status=AssetStatus(model.status),
        purchase_cost=Decimal(model.purchase_cost),
        purchase_date=model.purchase_date,
        salvage_value=Decimal(model.salvage_value),
        useful_life_months=model.useful_life_months,
        depreciation_method=DepreciationMethod(model.depreciation_method),
        description=model.description,
        assigned_to_user_id=model.assigned_to_user_id,
        metadata=model.asset_metadata,
        created_at=model.created_at,
        updated_at=model.updated_at,
        deleted_at=model.deleted_at,
    )
