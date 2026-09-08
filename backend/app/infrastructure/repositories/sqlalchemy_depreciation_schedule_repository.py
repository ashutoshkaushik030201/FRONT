import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.depreciation_schedule import DepreciationSchedule
from app.domain.repositories.depreciation_schedule_repository import DepreciationScheduleRepository
from app.infrastructure.db.models.depreciation_schedule_model import DepreciationScheduleModel


class SqlAlchemyDepreciationScheduleRepository(DepreciationScheduleRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_asset(self, asset_id: uuid.UUID) -> list[DepreciationSchedule]:
        stmt = (
            select(DepreciationScheduleModel)
            .where(DepreciationScheduleModel.asset_id == asset_id)
            .order_by(DepreciationScheduleModel.period_start.asc())
        )
        models = (await self._session.execute(stmt)).scalars().all()
        return [_to_entity(model) for model in models]

    async def replace_for_asset(
        self, asset_id: uuid.UUID, schedules: list[DepreciationSchedule]
    ) -> list[DepreciationSchedule]:
        await self._session.execute(
            delete(DepreciationScheduleModel).where(DepreciationScheduleModel.asset_id == asset_id)
        )
        models = [
            DepreciationScheduleModel(
                asset_id=schedule.asset_id,
                period_start=schedule.period_start,
                period_end=schedule.period_end,
                opening_book_value=schedule.opening_book_value,
                depreciation_amount=schedule.depreciation_amount,
                closing_book_value=schedule.closing_book_value,
            )
            for schedule in schedules
        ]
        self._session.add_all(models)
        await self._session.flush()
        for model in models:
            await self._session.refresh(model)
        return [_to_entity(model) for model in models]


def _to_entity(model: DepreciationScheduleModel) -> DepreciationSchedule:
    return DepreciationSchedule(
        id=model.id,
        asset_id=model.asset_id,
        period_start=model.period_start,
        period_end=model.period_end,
        opening_book_value=model.opening_book_value,
        depreciation_amount=model.depreciation_amount,
        closing_book_value=model.closing_book_value,
        created_at=model.created_at,
    )
