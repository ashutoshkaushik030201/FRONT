from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.depreciation_schedule import DepreciationSchedule


class DepreciationScheduleRepository(ABC):
    """Port defining persistence operations for computed depreciation schedules."""

    @abstractmethod
    async def list_by_asset(self, asset_id: UUID) -> list[DepreciationSchedule]: ...

    @abstractmethod
    async def replace_for_asset(
        self, asset_id: UUID, schedules: list[DepreciationSchedule]
    ) -> list[DepreciationSchedule]: ...
