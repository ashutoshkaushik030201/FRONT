from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.asset import Asset


class AssetRepository(ABC):
    """Port defining persistence operations required by asset use cases."""

    @abstractmethod
    async def get_by_id(self, asset_id: UUID) -> Asset | None: ...

    @abstractmethod
    async def get_by_tag(self, asset_tag: str) -> Asset | None: ...

    @abstractmethod
    async def list(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        category_id: UUID | None = None,
        status: str | None = None,
        sort_by: str | None = None,
        sort_order: str = "asc",
    ) -> tuple[list[Asset], int]: ...

    @abstractmethod
    async def create(self, asset: Asset) -> Asset: ...

    @abstractmethod
    async def update(self, asset: Asset) -> Asset: ...

    @abstractmethod
    async def soft_delete(self, asset_id: UUID) -> None: ...
