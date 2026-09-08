import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from app.domain.entities.asset_assignment import AssetAssignment
from app.domain.exceptions import EntityNotFoundError, InvalidOperationError
from app.domain.repositories.asset_assignment_repository import AssetAssignmentRepository
from app.domain.repositories.asset_repository import AssetRepository
from app.domain.repositories.user_repository import UserRepository


@dataclass
class AssignAssetInput:
    asset_id: uuid.UUID
    user_id: uuid.UUID
    notes: str | None = None


class AssignAssetUseCase:
    """Assigns an asset to a user: closes any open assignment and records new history atomically."""

    def __init__(
        self,
        asset_repository: AssetRepository,
        user_repository: UserRepository,
        assignment_repository: AssetAssignmentRepository,
    ) -> None:
        self._asset_repository = asset_repository
        self._user_repository = user_repository
        self._assignment_repository = assignment_repository

    async def execute(self, data: AssignAssetInput) -> AssetAssignment:
        asset = await self._asset_repository.get_by_id(data.asset_id)
        if asset is None or asset.is_deleted:
            raise EntityNotFoundError("Asset", data.asset_id)

        user = await self._user_repository.get_by_id(data.user_id)
        if user is None or not user.is_active:
            raise EntityNotFoundError("User", data.user_id)

        if asset.is_assigned and asset.assigned_to_user_id == data.user_id:
            raise InvalidOperationError("Asset is already assigned to this user")

        now = datetime.now(timezone.utc)

        # Both the assignment close-out and the asset/history writes share one request-scoped
        # session/transaction (see infrastructure.db.session.get_db), so this is atomic.
        if asset.is_assigned:
            await self._assignment_repository.close_open_assignment(asset.id, returned_at=now)

        asset.assigned_to_user_id = data.user_id
        await self._asset_repository.update(asset)

        assignment = AssetAssignment(
            id=None,
            asset_id=data.asset_id,
            user_id=data.user_id,
            assigned_at=now,
            notes=data.notes,
        )
        return await self._assignment_repository.create(assignment)
