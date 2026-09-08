import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.asset_category import AssetCategory
from app.domain.repositories.asset_category_repository import AssetCategoryRepository
from app.infrastructure.db.models.asset_category_model import AssetCategoryModel


class SqlAlchemyAssetCategoryRepository(AssetCategoryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list(self) -> list[AssetCategory]:
        stmt = select(AssetCategoryModel).order_by(AssetCategoryModel.name.asc())
        models = (await self._session.execute(stmt)).scalars().all()
        return [_to_entity(model) for model in models]

    async def get_by_id(self, category_id: uuid.UUID) -> AssetCategory | None:
        model = await self._session.get(AssetCategoryModel, category_id)
        return _to_entity(model) if model else None


def _to_entity(model: AssetCategoryModel) -> AssetCategory:
    return AssetCategory(id=model.id, name=model.name, type=model.type)
