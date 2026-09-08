from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.audit_log import AuditLog


class AuditRepository(ABC):
    """Port defining persistence operations for audit trail entries."""

    @abstractmethod
    async def create(self, audit_log: AuditLog) -> AuditLog: ...

    @abstractmethod
    async def list(
        self,
        *,
        page: int,
        page_size: int,
        entity_type: str | None = None,
        entity_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> tuple[list[AuditLog], int]: ...
