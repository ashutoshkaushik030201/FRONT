import uuid
from dataclasses import dataclass

from app.domain.entities.audit_log import AuditAction, AuditLog
from app.domain.repositories.audit_repository import AuditRepository


@dataclass
class RecordAuditEventInput:
    action: AuditAction
    entity_type: str
    entity_id: uuid.UUID
    user_id: uuid.UUID | None = None
    old_values: dict | None = None
    new_values: dict | None = None
    ip_address: str | None = None


class RecordAuditEventUseCase:
    def __init__(self, audit_repository: AuditRepository) -> None:
        self._audit_repository = audit_repository

    async def execute(self, data: RecordAuditEventInput) -> AuditLog:
        audit_log = AuditLog(
            id=None,
            action=data.action,
            entity_type=data.entity_type,
            entity_id=data.entity_id,
            user_id=data.user_id,
            old_values=data.old_values or {},
            new_values=data.new_values or {},
            ip_address=data.ip_address,
        )
        return await self._audit_repository.create(audit_log)
