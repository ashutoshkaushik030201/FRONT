import uuid
from dataclasses import dataclass

from app.domain.entities.asset import Asset
from app.domain.repositories.asset_repository import AssetRepository


@dataclass
class ListAssetsResult:
    items: list[Asset]
    total: int
    page: int
    page_size: int


class ListAssetsUseCase:
    """Orchestrates paginated, filtered, sorted, full-text-searchable asset retrieval."""

    def __init__(self, asset_repository: AssetRepository) -> None:
        self._asset_repository = asset_repository

    async def execute(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        category_id: uuid.UUID | None = None,
        status: str | None = None,
        sort_by: str | None = None,
        sort_order: str = "asc",
    ) -> ListAssetsResult:
        items, total = await self._asset_repository.list(
            page=page,
            page_size=page_size,
            search=search,
            category_id=category_id,
            status=status,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        return ListAssetsResult(items=items, total=total, page=page, page_size=page_size)
