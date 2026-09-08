from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID


class AuditAction(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


@dataclass
class AuditLog:
    id: UUID | None
    action: AuditAction
    entity_type: str
    entity_id: UUID
    user_id: UUID | None = None
    old_values: dict = field(default_factory=dict)
    new_values: dict = field(default_factory=dict)
    ip_address: str | None = None
    created_at: datetime | None = None
