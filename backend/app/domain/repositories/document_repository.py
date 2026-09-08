from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.document import Document


class DocumentRepository(ABC):
    """Port defining persistence operations for asset-linked documents."""

    @abstractmethod
    async def get_by_id(self, document_id: UUID) -> Document | None: ...

    @abstractmethod
    async def list_by_asset(self, asset_id: UUID) -> list[Document]: ...

    @abstractmethod
    async def create(self, document: Document) -> Document: ...

    @abstractmethod
    async def delete(self, document_id: UUID) -> None: ...
