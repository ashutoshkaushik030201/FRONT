from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.asset_category import AssetCategory


class AssetCategoryRepository(ABC):
    """Port defining read access to asset categories."""

    @abstractmethod
    async def list(self) -> list[AssetCategory]: ...

    @abstractmethod
    async def get_by_id(self, category_id: UUID) -> AssetCategory | None: ...
