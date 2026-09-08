from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class RoleName(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    VIEWER = "viewer"


@dataclass
class User:
    id: UUID | None
    email: str
    hashed_password: str
    full_name: str
    role_id: UUID
    # Denormalized from the joined Role row; kept on the entity for convenient RBAC checks.
    role_name: str
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None
