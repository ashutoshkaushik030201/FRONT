import uuid
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.asset_assignment import AssetAssignment
from app.domain.repositories.asset_assignment_repository import AssetAssignmentRepository
from app.infrastructure.db.models.asset_assignment_model import AssetAssignmentModel


class SqlAlchemyAssetAssignmentRepository(AssetAssignmentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, assignment: AssetAssignment) -> AssetAssignment:
        model = AssetAssignmentModel(
            asset_id=assignment.asset_id,
            user_id=assignment.user_id,
            assigned_at=assignment.assigned_at,
            returned_at=assignment.returned_at,
            notes=assignment.notes,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def list_by_asset(self, asset_id: uuid.UUID) -> list[AssetAssignment]:
        stmt = (
            select(AssetAssignmentModel)
            .where(AssetAssignmentModel.asset_id == asset_id)
            .order_by(AssetAssignmentModel.assigned_at.desc())
        )
        models = (await self._session.execute(stmt)).scalars().all()
        return [_to_entity(model) for model in models]

    async def close_open_assignment(self, asset_id: uuid.UUID, *, returned_at: datetime) -> None:
        stmt = (
            update(AssetAssignmentModel)
            .where(
                AssetAssignmentModel.asset_id == asset_id,
                AssetAssignmentModel.returned_at.is_(None),
            )
            .values(returned_at=returned_at)
        )
        await self._session.execute(stmt)


def _to_entity(model: AssetAssignmentModel) -> AssetAssignment:
    return AssetAssignment(
        id=model.id,
        asset_id=model.asset_id,
        user_id=model.user_id,
        assigned_at=model.assigned_at,
        returned_at=model.returned_at,
        notes=model.notes,
    )
