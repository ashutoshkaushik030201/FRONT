from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from app.domain.entities.asset_assignment import AssetAssignment


class AssetAssignmentRepository(ABC):
    """Port defining persistence operations for asset assignment history."""

    @abstractmethod
    async def create(self, assignment: AssetAssignment) -> AssetAssignment: ...

    @abstractmethod
    async def list_by_asset(self, asset_id: UUID) -> list[AssetAssignment]: ...

    @abstractmethod
    async def close_open_assignment(self, asset_id: UUID, *, returned_at: datetime) -> None: ...
